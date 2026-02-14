'use client'

import { useState, useEffect } from 'react'
import ResourceMap from './ResourceMap'
import StatsCards from './StatsCards'
import ResourceList from './ResourceList'
import { Map as MapIcon, List } from 'lucide-react'

export default function Dashboard() {
  const [viewMode, setViewMode] = useState<'map' | 'list'>('map')
  const [selectedResourceType, setSelectedResourceType] = useState<string>('all')

  return (
    <div className="space-y-6">
      {/* View Toggle */}
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold text-gray-800">Resource Distribution</h2>
        <div className="flex items-center space-x-2">
          <div className="bg-white rounded-lg shadow-sm p-1 flex">
            <button
              onClick={() => setViewMode('map')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                viewMode === 'map'
                  ? 'bg-primary-600 text-white'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <MapIcon className="w-5 h-5" />
              <span>Map View</span>
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                viewMode === 'list'
                  ? 'bg-primary-600 text-white'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <List className="w-5 h-5" />
              <span>List View</span>
            </button>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <StatsCards />

      {/* Resource Type Filter */}
      <div className="bg-white rounded-lg shadow-sm p-4">
        <div className="flex items-center space-x-4">
          <span className="text-sm font-medium text-gray-700">Filter by Resource:</span>
          <div className="flex flex-wrap gap-2">
            {['all', 'water', 'health', 'education', 'agriculture'].map((type) => (
              <button
                key={type}
                onClick={() => setSelectedResourceType(type)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  selectedResourceType === type
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {type.charAt(0).toUpperCase() + type.slice(1)}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="bg-white rounded-lg shadow-sm overflow-hidden">
        {viewMode === 'map' ? (
          <ResourceMap resourceType={selectedResourceType} />
        ) : (
          <ResourceList resourceType={selectedResourceType} />
        )}
      </div>
    </div>
  )
}
