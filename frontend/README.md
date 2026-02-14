# Smart City FIS - Frontend Dashboard

A modern React/Next.js dashboard with interactive maps for visualizing resource distribution in Tanzania's Smart City system.

## Features

- **Interactive Map View**: Leaflet-based map showing resource distribution across Tanzania
- **Resource Types**: Water, Health, Education, and Agriculture resources
- **Stats Dashboard**: Real-time statistics cards showing resource counts
- **List View**: Alternative list view for detailed resource information
- **Filtering**: Filter resources by type (water, health, education, agriculture)
- **Responsive Design**: Tailwind CSS-based responsive layout

## Technology Stack

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Leaflet/React-Leaflet**: Interactive map library
- **Lucide React**: Icon library
- **Axios**: HTTP client for API calls

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn
- Backend API running (see backend README)

### Installation

1. Install dependencies:
```bash
npm install
```

2. Copy environment file:
```bash
cp .env.example .env
```

3. Update `.env` with your API URL:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_MAPBOX_TOKEN=your-mapbox-token-if-using-mapbox
```

### Development

Run the development server:
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx       # Root layout
│   ├── page.tsx         # Main dashboard page
│   └── globals.css      # Global styles
├── components/
│   ├── Dashboard.tsx    # Main dashboard component
│   ├── Header.tsx       # Top navigation header
│   ├── Sidebar.tsx      # Side navigation
│   ├── ResourceMap.tsx  # Interactive map component
│   ├── ResourceList.tsx # List view component
│   └── StatsCards.tsx   # Statistics cards
├── lib/
│   └── api.ts           # API client utilities
├── public/              # Static assets
└── ...config files
```

## Components

### Dashboard
Main component that manages view modes (map/list) and resource filtering.

### ResourceMap
Interactive Leaflet map showing:
- Resource markers with custom icons by type
- Coverage circles based on capacity
- Popups with resource details
- Legend for resource types

### ResourceList
List view displaying resources in a table format with:
- Resource details
- Capacity information
- Status indicators
- Location information

### StatsCards
Statistics dashboard showing:
- Total counts by resource type
- Trend indicators
- Quick overview metrics

## Map Configuration

The map is centered on Tanzania (Dar es Salaam) and uses OpenStreetMap tiles. To use Mapbox instead:

1. Get a Mapbox token from [mapbox.com](https://www.mapbox.com)
2. Update `.env` with `NEXT_PUBLIC_MAPBOX_TOKEN`
3. Modify `ResourceMap.tsx` to use Mapbox tiles

## API Integration

The frontend expects the following API endpoints:

- `GET /api/v1/resources` - List all resources
- `GET /api/v1/resources/{id}` - Get resource details
- `GET /api/v1/resources/nearby` - Get resources near location
- `GET /api/v1/analytics/stats` - Get statistics
- `GET /api/v1/ingestion/sources` - List data sources

See `lib/api.ts` for the complete API client implementation.

## Customization

### Adding New Resource Types

1. Update `ResourceMap.tsx` with new icon and color:
```typescript
const icons = {
  water: createCustomIcon('#0ea5e9', 'W'),
  health: createCustomIcon('#ef4444', 'H'),
  education: createCustomIcon('#10b981', 'E'),
  agriculture: createCustomIcon('#f59e0b', 'A'),
  newtype: createCustomIcon('#yourcolor', 'N'), // Add here
}
```

2. Update `StatsCards.tsx` to include new type in stats
3. Update `ResourceList.tsx` to handle new type

### Styling

All styles use Tailwind CSS. Modify `tailwind.config.js` to customize:
- Color scheme
- Spacing
- Typography
- Components

## Docker Support

The frontend can be run in Docker. See `Dockerfile` for details.

```bash
docker build -t smartcity-frontend .
docker run -p 3000:3000 smartcity-frontend
```

## Troubleshooting

### Map not displaying
- Check browser console for Leaflet CSS import
- Verify OpenStreetMap tiles are accessible
- Check network connectivity

### API errors
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check backend API is running
- Verify CORS settings on backend

### Build errors
- Clear `.next` folder and rebuild
- Check Node.js version (18+)
- Verify all dependencies are installed

## License

See main project LICENSE file.
