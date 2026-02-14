'use client'

import { useEffect, useState } from 'react'
import { Droplet, Heart, GraduationCap, Wheat, MapPin, ChevronRight } from 'lucide-react'

interface Resource {
  id: string
  name: string
  type: string
  location: string
  capacity?: number
  currentLevel?: number
  status: string
  lastUpdated: string
}

interface ResourceListProps {
  resourceType: string
}

export default function ResourceList({ resourceType }: ResourceListProps) {
  const [resources, setResources] = useState<Resource[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchResources = async () => {
      setLoading(true)
      try {
        // Mock data - replace with actual API call
        const mockResources: Resource[] = [
          {
            id: '1',
            name: 'Dar es Salaam Water Treatment Plant',
            type: 'water',
            location: 'Dar es Salaam',
            capacity: 500000,
            currentLevel: 350000,
            status: 'operational',
            lastUpdated: '2024-01-15',
          },
          {
            id: '2',
            name: 'Arusha Water Reservoir',
            type: 'water',
            location: 'Arusha',
            capacity: 200000,
            currentLevel: 120000,
            status: 'operational',
            lastUpdated: '2024-01-15',
          },
          {
            id: '3',
            name: 'Muhimbili National Hospital',
            type: 'health',
            location: 'Dar es Salaam',
            capacity: 1500,
            status: 'operational',
            lastUpdated: '2024-01-14',
          },
          {
            id: '4',
            name: 'Kilimanjaro Christian Medical Centre',
            type: 'health',
            location: 'Moshi',
            capacity: 500,
            status: 'operational',
            lastUpdated: '2024-01-14',
          },
          {
            id: '5',
            name: 'University of Dar es Salaam',
            type: 'education',
            location: 'Dar es Salaam',
            capacity: 25000,
            status: 'operational',
            lastUpdated: '2024-01-13',
          },
          {
            id: '6',
            name: 'Arusha Secondary School',
            type: 'education',
            location: 'Arusha',
            capacity: 1200,
            status: 'operational',
            lastUpdated: '2024-01-13',
          },
          {
            id: '7',
            name: 'Kilimanjaro Coffee Farm',
            type: 'agriculture',
            location: 'Kilimanjaro',
            capacity: 500,
            status: 'operational',
            lastUpdated: '2024-01-12',
          },
        ]

        const filtered = resourceType === 'all'
          ? mockResources
          : mockResources.filter((r) => r.type === resourceType)

        setResources(filtered)
      } catch (error) {
        console.error('Error fetching resources:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchResources()
  }, [resourceType])

  const getResourceIcon = (type: string) => {
    const icons = {
      water: Droplet,
      health: Heart,
      education: GraduationCap,
      agriculture: Wheat,
    }
    return icons[type as keyof typeof icons] || MapPin
  }

  const getResourceColor = (type: string) => {
    const colors = {
      water: 'text-blue-600 bg-blue-50',
      health: 'text-red-600 bg-red-50',
      education: 'text-green-600 bg-green-50',
      agriculture: 'text-yellow-600 bg-yellow-50',
    }
    return colors[type as keyof typeof colors] || 'text-gray-600 bg-gray-50'
  }

  const getStatusColor = (status: string) => {
    return status === 'operational'
      ? 'bg-green-100 text-green-800'
      : 'bg-red-100 text-red-800'
  }

  if (loading) {
    return (
      <div className="h-[600px] flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading resources...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="overflow-y-auto max-h-[600px]">
      <div className="divide-y divide-gray-200">
        {resources.map((resource) => {
          const Icon = getResourceIcon(resource.type)
          const colorClass = getResourceColor(resource.type)

          return (
            <div
              key={resource.id}
              className="p-6 hover:bg-gray-50 transition-colors cursor-pointer"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4 flex-1">
                  <div className={`${colorClass} p-3 rounded-lg`}>
                    <Icon className="w-6 h-6" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {resource.name}
                    </h3>
                    <div className="flex items-center space-x-4 mt-2">
                      <div className="flex items-center space-x-1 text-sm text-gray-600">
                        <MapPin className="w-4 h-4" />
                        <span>{resource.location}</span>
                      </div>
                      <span className="text-sm text-gray-500 capitalize">
                        {resource.type}
                      </span>
                      <span
                        className={`text-xs px-2 py-1 rounded-full font-medium ${getStatusColor(
                          resource.status
                        )}`}
                      >
                        {resource.status}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center space-x-6">
                  {resource.capacity && (
                    <div className="text-right">
                      <p className="text-sm text-gray-600">Capacity</p>
                      <p className="text-lg font-semibold text-gray-900">
                        {resource.capacity.toLocaleString()}
                      </p>
                    </div>
                  )}
                  {resource.currentLevel !== undefined && (
                    <div className="text-right">
                      <p className="text-sm text-gray-600">Current Level</p>
                      <p className="text-lg font-semibold text-gray-900">
                        {Math.round(
                          (resource.currentLevel / resource.capacity!) * 100
                        )}
                        %
                      </p>
                    </div>
                  )}
                  <ChevronRight className="w-5 h-5 text-gray-400" />
                </div>
              </div>
            </div>
          )
        })}
      </div>
      {resources.length === 0 && (
        <div className="p-12 text-center text-gray-500">
          <p>No resources found for the selected filter.</p>
        </div>
      )}
    </div>
  )
}
