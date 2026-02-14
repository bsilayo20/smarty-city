'use client'

import { useEffect, useState, useRef } from 'react'
import { MapContainer, TileLayer, Marker, Popup, Circle, useMap } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { Droplet, Heart, GraduationCap, Wheat, MapPin } from 'lucide-react'
import axios from 'axios'

// Fix for default marker icons in Next.js
delete (L.Icon.Default.prototype as any)._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
})

// Custom icon component
const createCustomIcon = (color: string, type: string) => {
  return L.divIcon({
    className: 'custom-marker',
    html: `
      <div style="
        background-color: ${color};
        width: 30px;
        height: 30px;
        border-radius: 50%;
        border: 3px solid white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
      ">
        <span style="font-size: 16px;">${type.charAt(0).toUpperCase()}</span>
      </div>
    `,
    iconSize: [30, 30],
    iconAnchor: [15, 15],
  })
}

interface Resource {
  id: string
  name: string
  type: string
  latitude: number
  longitude: number
  capacity?: number
  currentLevel?: number
  population?: number
  description?: string
}

interface ResourceMapProps {
  resourceType: string
}

// Map center on Tanzania (Dar es Salaam)
const TANZANIA_CENTER: [number, number] = [-6.7924, 39.2083]
const DEFAULT_ZOOM = 7

function MapController({ center, zoom }: { center: [number, number], zoom: number }) {
  const map = useMap()
  useEffect(() => {
    map.setView(center, zoom)
  }, [map, center, zoom])
  return null
}

export default function ResourceMap({ resourceType }: ResourceMapProps) {
  const [resources, setResources] = useState<Resource[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedResource, setSelectedResource] = useState<Resource | null>(null)
  const mapRef = useRef<L.Map | null>(null)

  // Fetch resources from API
  useEffect(() => {
    const fetchResources = async () => {
      setLoading(true)
      try {
        // Mock data for demonstration - replace with actual API call
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        
        // In production, replace with:
        // const response = await axios.get(`${apiUrl}/api/v1/resources`, {
        //   params: { type: resourceType === 'all' ? undefined : resourceType }
        // })
        
        // Mock data for demonstration
        const mockResources: Resource[] = [
          // Water Resources
          {
            id: '1',
            name: 'Dar es Salaam Water Treatment Plant',
            type: 'water',
            latitude: -6.7924,
            longitude: 39.2083,
            capacity: 500000,
            currentLevel: 350000,
            description: 'Main water treatment facility serving Dar es Salaam'
          },
          {
            id: '2',
            name: 'Arusha Water Reservoir',
            type: 'water',
            latitude: -3.3869,
            longitude: 36.6830,
            capacity: 200000,
            currentLevel: 120000,
            description: 'Water storage for Arusha region'
          },
          // Health Resources
          {
            id: '3',
            name: 'Muhimbili National Hospital',
            type: 'health',
            latitude: -6.7944,
            longitude: 39.2081,
            capacity: 1500,
            population: 500000,
            description: 'Largest referral hospital in Tanzania'
          },
          {
            id: '4',
            name: 'Kilimanjaro Christian Medical Centre',
            type: 'health',
            latitude: -3.2833,
            longitude: 37.3333,
            capacity: 500,
            population: 200000,
            description: 'Regional hospital in Moshi'
          },
          // Education Resources
          {
            id: '5',
            name: 'University of Dar es Salaam',
            type: 'education',
            latitude: -6.7791,
            longitude: 39.2096,
            capacity: 25000,
            description: 'Leading university in Tanzania'
          },
          {
            id: '6',
            name: 'Arusha Secondary School',
            type: 'education',
            latitude: -3.3869,
            longitude: 36.6830,
            capacity: 1200,
            description: 'Secondary school in Arusha'
          },
          // Agriculture
          {
            id: '7',
            name: 'Kilimanjaro Coffee Farm',
            type: 'agriculture',
            latitude: -3.0667,
            longitude: 37.3500,
            capacity: 500,
            description: 'Coffee plantation in Kilimanjaro region'
          },
        ]

        // Filter by resource type
        const filtered = resourceType === 'all' 
          ? mockResources 
          : mockResources.filter(r => r.type === resourceType)
        
        setResources(filtered)
      } catch (error) {
        console.error('Error fetching resources:', error)
        // Fallback to mock data on error
      } finally {
        setLoading(false)
      }
    }

    fetchResources()
  }, [resourceType])

  const getResourceIcon = (type: string) => {
    const icons = {
      water: createCustomIcon('#0ea5e9', 'W'),
      health: createCustomIcon('#ef4444', 'H'),
      education: createCustomIcon('#10b981', 'E'),
      agriculture: createCustomIcon('#f59e0b', 'A'),
    }
    return icons[type as keyof typeof icons] || createCustomIcon('#6b7280', 'R')
  }

  const getResourceColor = (type: string) => {
    const colors = {
      water: '#0ea5e9',
      health: '#ef4444',
      education: '#10b981',
      agriculture: '#f59e0b',
    }
    return colors[type as keyof typeof colors] || '#6b7280'
  }

  if (loading) {
    return (
      <div className="h-[600px] flex items-center justify-center bg-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading map resources...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="relative h-[600px] w-full">
      <MapContainer
        center={TANZANIA_CENTER}
        zoom={DEFAULT_ZOOM}
        style={{ height: '100%', width: '100%', zIndex: 0 }}
        ref={mapRef}
        scrollWheelZoom={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        <MapController center={TANZANIA_CENTER} zoom={DEFAULT_ZOOM} />

        {resources.map((resource) => (
          <div key={resource.id}>
            <Marker
              position={[resource.latitude, resource.longitude]}
              icon={getResourceIcon(resource.type)}
              eventHandlers={{
                click: () => setSelectedResource(resource),
              }}
            >
              <Popup>
                <div className="p-2 min-w-[200px]">
                  <h3 className="font-bold text-lg mb-2">{resource.name}</h3>
                  <div className="space-y-1 text-sm">
                    <p className="capitalize">
                      <span className="font-medium">Type:</span> {resource.type}
                    </p>
                    {resource.capacity && (
                      <p>
                        <span className="font-medium">Capacity:</span> {resource.capacity.toLocaleString()}
                      </p>
                    )}
                    {resource.currentLevel && (
                      <p>
                        <span className="font-medium">Current Level:</span>{' '}
                        {resource.currentLevel.toLocaleString()} (
                        {Math.round((resource.currentLevel / resource.capacity!) * 100)}%)
                      </p>
                    )}
                    {resource.population && (
                      <p>
                        <span className="font-medium">Serves:</span>{' '}
                        {resource.population.toLocaleString()} people
                      </p>
                    )}
                    {resource.description && (
                      <p className="text-gray-600 mt-2">{resource.description}</p>
                    )}
                  </div>
                </div>
              </Popup>
            </Marker>

            {/* Circle showing coverage area */}
            {resource.capacity && (
              <Circle
                center={[resource.latitude, resource.longitude]}
                radius={resource.capacity / 10} // Scale radius based on capacity
                pathOptions={{
                  color: getResourceColor(resource.type),
                  fillColor: getResourceColor(resource.type),
                  fillOpacity: 0.1,
                  weight: 2,
                }}
              />
            )}
          </div>
        ))}
      </MapContainer>

      {/* Legend */}
      <div className="absolute bottom-4 right-4 bg-white rounded-lg shadow-lg p-4 z-[1000]">
        <h4 className="font-bold text-sm mb-2">Resource Types</h4>
        <div className="space-y-2 text-sm">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-blue-500 rounded-full"></div>
            <span>Water</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-red-500 rounded-full"></div>
            <span>Health</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-green-500 rounded-full"></div>
            <span>Education</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-yellow-500 rounded-full"></div>
            <span>Agriculture</span>
          </div>
        </div>
      </div>
    </div>
  )
}
