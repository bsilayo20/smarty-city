'use client'

import { useEffect, useState } from 'react'
import { Droplet, Heart, GraduationCap, Wheat, TrendingUp, MapPin } from 'lucide-react'

interface Stats {
  water: number
  health: number
  education: number
  agriculture: number
  total: number
}

export default function StatsCards() {
  const [stats, setStats] = useState<Stats>({
    water: 0,
    health: 0,
    education: 0,
    agriculture: 0,
    total: 0,
  })

  useEffect(() => {
    // Fetch stats from API
    // Mock data for now
    setStats({
      water: 24,
      health: 18,
      education: 42,
      agriculture: 31,
      total: 115,
    })
  }, [])

  const cards = [
    {
      title: 'Water Resources',
      value: stats.water,
      icon: Droplet,
      color: 'bg-blue-500',
      bgColor: 'bg-blue-50',
      textColor: 'text-blue-600',
      trend: '+12%',
    },
    {
      title: 'Health Facilities',
      value: stats.health,
      icon: Heart,
      color: 'bg-red-500',
      bgColor: 'bg-red-50',
      textColor: 'text-red-600',
      trend: '+5%',
    },
    {
      title: 'Education Centers',
      value: stats.education,
      icon: GraduationCap,
      color: 'bg-green-500',
      bgColor: 'bg-green-50',
      textColor: 'text-green-600',
      trend: '+8%',
    },
    {
      title: 'Agriculture Sites',
      value: stats.agriculture,
      icon: Wheat,
      color: 'bg-yellow-500',
      bgColor: 'bg-yellow-50',
      textColor: 'text-yellow-600',
      trend: '+15%',
    },
    {
      title: 'Total Resources',
      value: stats.total,
      icon: MapPin,
      color: 'bg-purple-500',
      bgColor: 'bg-purple-50',
      textColor: 'text-purple-600',
      trend: '+10%',
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
      {cards.map((card) => {
        const Icon = card.icon
        return (
          <div
            key={card.title}
            className={`${card.bgColor} rounded-lg shadow-sm p-6 border border-gray-100 hover:shadow-md transition-shadow`}
          >
            <div className="flex items-center justify-between mb-4">
              <div className={`${card.color} p-3 rounded-lg`}>
                <Icon className="w-6 h-6 text-white" />
              </div>
              <div className="flex items-center space-x-1 text-sm text-gray-600">
                <TrendingUp className="w-4 h-4" />
                <span className="font-medium">{card.trend}</span>
              </div>
            </div>
            <div className="space-y-1">
              <p className={`text-3xl font-bold ${card.textColor}`}>
                {card.value.toLocaleString()}
              </p>
              <p className="text-sm text-gray-600 font-medium">{card.title}</p>
            </div>
          </div>
        )
      })}
    </div>
  )
}
