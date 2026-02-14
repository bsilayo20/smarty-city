'use client'

import { 
  LayoutDashboard, 
  Map, 
  Database, 
  BarChart3, 
  Settings, 
  Activity,
  Droplet,
  Heart,
  GraduationCap,
  Building2
} from 'lucide-react'
import { useState } from 'react'

const menuItems = [
  { icon: LayoutDashboard, label: 'Dashboard', active: true },
  { icon: Map, label: 'Map View', active: false },
  { icon: Database, label: 'Data Sources', active: false },
  { icon: BarChart3, label: 'Analytics', active: false },
  { icon: Activity, label: 'Resources', active: false },
  { icon: Droplet, label: 'Water', active: false },
  { icon: Heart, label: 'Health', active: false },
  { icon: GraduationCap, label: 'Education', active: false },
  { icon: Building2, label: 'Infrastructure', active: false },
  { icon: Settings, label: 'Settings', active: false },
]

export default function Sidebar() {
  const [activeItem, setActiveItem] = useState('Dashboard')

  return (
    <aside className="w-64 bg-gray-900 text-white flex flex-col">
      <div className="p-6 border-b border-gray-800">
        <h2 className="text-xl font-bold text-white">Smart City FIS</h2>
        <p className="text-sm text-gray-400 mt-1">Tanzania</p>
      </div>
      
      <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
        {menuItems.map((item) => {
          const Icon = item.icon
          const isActive = activeItem === item.label
          
          return (
            <button
              key={item.label}
              onClick={() => setActiveItem(item.label)}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? 'bg-primary-600 text-white'
                  : 'text-gray-300 hover:bg-gray-800 hover:text-white'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span className="font-medium">{item.label}</span>
            </button>
          )
        })}
      </nav>
      
      <div className="p-4 border-t border-gray-800">
        <div className="bg-gray-800 rounded-lg p-3">
          <p className="text-sm text-gray-300">System Status</p>
          <div className="flex items-center space-x-2 mt-2">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-xs text-gray-400">All systems operational</span>
          </div>
        </div>
      </div>
    </aside>
  )
}
