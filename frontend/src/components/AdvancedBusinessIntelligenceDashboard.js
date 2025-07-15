import React, { useState, useEffect } from 'react';
import { 
  LineChart, Line, AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  ComposedChart, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar
} from 'recharts';
import { 
  TrendingUp, DollarSign, Users, ShoppingCart, Globe, Cpu, Zap, 
  Award, BarChart3, Activity, Target, ArrowUp, ArrowDown, Minus,
  Download, Share2, RefreshCw
} from 'lucide-react';

const AdvancedBusinessIntelligenceDashboard = () => {
  const [timeRange, setTimeRange] = useState('7d');
  const [selectedMetrics, setSelectedMetrics] = useState(['revenue', 'users', 'conversion']);
  const [realTimeData, setRealTimeData] = useState({});
  const [autoRefresh, setAutoRefresh] = useState(true);

  const [businessMetrics] = useState({
    revenue: { current: 2847500, change: 32.7 },
    users: { total: 127543, active: 89234, new: 12456 },
    conversion: { overall: 0.078, mobile: 0.065, desktop: 0.089 },
    recommendations: { ctr: 0.347, accuracy: 0.867, satisfaction: 4.6 },
    performance: { responseTime: 45, uptime: 99.97, cacheHitRate: 93.4 }
  });

  const [globalData] = useState({
    regions: [
      { name: 'North America', revenue: 1250000, users: 45000, growth: 24.5, flag: '🇺🇸' },
      { name: 'Europe', revenue: 890000, users: 38000, growth: 31.2, flag: '🇪🇺' },
      { name: 'Asia Pacific', revenue: 567000, users: 35000, growth: 48.7, flag: '🌏' }
    ]
  });

  const [mlMetrics] = useState({
    models: [
      { name: 'Collaborative Filtering', accuracy: 83.2 },
      { name: 'Deep Learning', accuracy: 87.1 },
      { name: 'Transformer', accuracy: 89.4 },
      { name: 'Ensemble', accuracy: 91.7 }
    ],
    experiments: [
      { name: 'Algorithm A vs B', status: 'completed', improvement: 12.3, confidence: 95 },
      { name: 'Real-time vs Batch', status: 'running', improvement: 8.7, confidence: 87 }
    ]
  });

  const [userAnalytics] = useState({
    demographics: [
      { age: '18-24', percentage: 18.5, color: '#8884d8' },
      { age: '25-34', percentage: 34.7, color: '#82ca9d' },
      { age: '35-44', percentage: 28.9, color: '#ffc658' },
      { age: '45-54', percentage: 12.8, color: '#ff7300' },
      { age: '55+', percentage: 5.1, color: '#00C49F' }
    ],
    devices: [
      { device: 'Mobile', users: 67834, percentage: 53.2 },
      { device: 'Desktop', users: 45678, percentage: 35.8 },
      { device: 'Tablet', users: 14031, percentage: 11.0 }
    ],
    trafficSources: [
      { source: 'Organic Search', percentage: 34.5, roas: 0 },
      { source: 'Paid Search', percentage: 28.7, roas: 3.2 },
      { source: 'Social Media', percentage: 15.8, roas: 2.1 },
      { source: 'Email', percentage: 12.3, roas: 8.7 }
    ]
  });

  useEffect(() => {
    const interval = setInterval(() => {
      if (autoRefresh) {
        setRealTimeData({
          timestamp: new Date().toISOString(),
          activeUsers: Math.floor(Math.random() * 500) + 2800,
          requestsPerSecond: Math.floor(Math.random() * 100) + 450,
          conversionRate: (Math.random() * 0.02 + 0.068).toFixed(4),
          responseTime: Math.floor(Math.random() * 20) + 35
        });
      }
    }, 3000);
    return () => clearInterval(interval);
  }, [autoRefresh]);

  const timeSeriesData = [
    { date: '2024-01-01', revenue: 125000, users: 8500, orders: 1200, conversion: 0.067 },
    { date: '2024-01-02', revenue: 132000, users: 8900, orders: 1340, conversion: 0.071 },
    { date: '2024-01-03', revenue: 145000, users: 9200, orders: 1450, conversion: 0.074 },
    { date: '2024-01-04', revenue: 139000, users: 8800, orders: 1390, conversion: 0.069 },
    { date: '2024-01-05', revenue: 158000, users: 9800, orders: 1580, conversion: 0.078 },
    { date: '2024-01-06', revenue: 167000, users: 10200, orders: 1670, conversion: 0.081 },
    { date: '2024-01-07', revenue: 172000, users: 10500, orders: 1720, conversion: 0.084 }
  ];

  const MetricCard = ({ title, value, change, icon: Icon, color = "blue", prefix = "", suffix = "" }) => (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className={`text-2xl font-bold text-${color}-600 mt-1`}>
            {prefix}{typeof value === 'number' ? value.toLocaleString() : value}{suffix}
          </p>
          {change !== undefined && (
            <div className="flex items-center mt-2">
              {change > 0 ? (
                <ArrowUp className="w-4 h-4 text-green-500 mr-1" />
              ) : change < 0 ? (
                <ArrowDown className="w-4 h-4 text-red-500 mr-1" />
              ) : (
                <Minus className="w-4 h-4 text-gray-500 mr-1" />
              )}
              <span className={`text-sm font-medium ${
                change > 0 ? 'text-green-600' : change < 0 ? 'text-red-600' : 'text-gray-600'
              }`}>
                {Math.abs(change)}%
              </span>
            </div>
          )}
        </div>
        <div className={`p-3 bg-${color}-100 rounded-lg`}>
          <Icon className={`w-6 h-6 text-${color}-600`} />
        </div>
      </div>
    </div>
  );

  const FilterPanel = () => (
    <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-800">Dashboard Controls</h3>
        <div className="flex space-x-2">
          <button
            onClick={() => setAutoRefresh(!autoRefresh)}
            className={`px-3 py-1 rounded text-sm font-medium ${
              autoRefresh ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'
            }`}
          >
            {autoRefresh ? 'Live' : 'Paused'}
          </button>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Time Range</label>
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
          >
            <option value="1d">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
            <option value="90d">Last 90 Days</option>
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Actions</label>
          <div className="flex space-x-2">
            <button className="flex-1 bg-blue-500 text-white px-3 py-2 rounded-lg text-sm hover:bg-blue-600 flex items-center justify-center">
              <Download className="w-4 h-4 mr-1" />
              Export
            </button>
            <button className="flex-1 bg-gray-500 text-white px-3 py-2 rounded-lg text-sm hover:bg-gray-600 flex items-center justify-center">
              <Share2 className="w-4 h-4 mr-1" />
              Share
            </button>
          </div>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Refresh</label>
          <button
            onClick={() => window.location.reload()}
            className="w-full bg-green-500 text-white px-3 py-2 rounded-lg text-sm hover:bg-green-600 flex items-center justify-center"
          >
            <RefreshCw className="w-4 h-4 mr-1" />
            Refresh All
          </button>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            SmartCommerce AI - Business Intelligence
          </h1>
          <p className="text-gray-600">
            Advanced analytics and insights for your AI-powered e-commerce platform
          </p>
          {realTimeData.timestamp && (
            <p className="text-sm text-gray-500 mt-2">
              Last updated: {new Date(realTimeData.timestamp).toLocaleTimeString()}
            </p>
          )}
        </div>

        <FilterPanel />

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <MetricCard
            title="Live Users"
            value={realTimeData.activeUsers || 3247}
            change={5.4}
            icon={Users}
            color="blue"
          />
          <MetricCard
            title="Requests/Sec"
            value={realTimeData.requestsPerSecond || 523}
            change={-2.1}
            icon={Activity}
            color="green"
          />
          <MetricCard
            title="Conversion Rate"
            value={realTimeData.conversionRate || "7.8%"}
            change={12.3}
            icon={Target}
            color="purple"
          />
          <MetricCard
            title="Response Time"
            value={realTimeData.responseTime || 45}
            change={-8.7}
            icon={Zap}
            color="orange"
            suffix="ms"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-800">Revenue Trend</h3>
              <span className="px-2 py-1 bg-green-100 text-green-800 rounded text-sm">
                +32.7% vs last period
              </span>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <ComposedChart data={timeSeriesData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis yAxisId="left" />
                <YAxis yAxisId="right" orientation="right" />
                <Tooltip />
                <Legend />
                <Area yAxisId="left" type="monotone" dataKey="revenue" stackId="1" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
                <Line yAxisId="right" type="monotone" dataKey="conversion" stroke="#ff7300" strokeWidth={2} />
              </ComposedChart>
            </ResponsiveContainer>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">User Growth</h3>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={timeSeriesData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Area type="monotone" dataKey="users" stackId="1" stroke="#82ca9d" fill="#82ca9d" />
                <Area type="monotone" dataKey="orders" stackId="1" stroke="#ffc658" fill="#ffc658" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">AI/ML Model Performance</h3>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-700 mb-3">Model Accuracy</h4>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={mlMetrics.models}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="accuracy" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div>
              <h4 className="font-medium text-gray-700 mb-3">A/B Test Results</h4>
              <div className="space-y-3">
                {mlMetrics.experiments.map((exp, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-3">
                    <div className="flex items-center justify-between">
                      <span className="font-medium text-sm">{exp.name}</span>
                      <span className={`px-2 py-1 rounded text-xs ${
                        exp.status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'
                      }`}>
                        {exp.status}
                      </span>
                    </div>
                    <div className="mt-2 flex items-center justify-between text-sm">
                      <span className="text-green-600 font-medium">+{exp.improvement}% improvement</span>
                      <span className="text-gray-600">{exp.confidence}% confidence</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Global Expansion Analytics</h3>
          <div className="space-y-3">
            {globalData.regions.map((region, index) => (
              <div key={index} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
                <div className="flex items-center">
                  <span className="text-2xl mr-3">{region.flag}</span>
                  <div>
                    <p className="font-medium text-sm">{region.name}</p>
                    <p className="text-xs text-gray-600">{region.users.toLocaleString()} users</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="font-bold text-sm">${(region.revenue / 1000).toFixed(0)}K</p>
                  <p className="text-xs text-green-600">+{region.growth}%</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">User Demographics</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={userAnalytics.demographics}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({age, percentage}) => `${age}: ${percentage}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="percentage"
                >
                  {userAnalytics.demographics.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Traffic Sources</h3>
            <div className="space-y-3">
              {userAnalytics.trafficSources.map((source, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="w-4 h-4 bg-blue-500 rounded mr-3" style={{backgroundColor: ['#8884d8', '#82ca9d', '#ffc658', '#ff7300'][index]}}></div>
                    <span className="text-sm font-medium">{source.source}</span>
                  </div>
                  <div className="text-right text-sm">
                    <div>{source.percentage}%</div>
                    {source.roas > 0 && (
                      <div className="text-xs text-green-600">ROAS: {source.roas}x</div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Recommendation Engine Performance</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <h4 className="font-medium text-gray-700 mb-3">Key Metrics</h4>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Click-through Rate</span>
                  <span className="font-medium">{(businessMetrics.recommendations.ctr * 100).toFixed(1)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Model Accuracy</span>
                  <span className="font-medium">{(businessMetrics.recommendations.accuracy * 100).toFixed(1)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">User Satisfaction</span>
                  <span className="font-medium">{businessMetrics.recommendations.satisfaction}/5.0</span>
                </div>
              </div>
            </div>

            <div>
              <h4 className="font-medium text-gray-700 mb-3">Device Performance</h4>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={userAnalytics.devices}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="device" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="percentage" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div>
              <h4 className="font-medium text-gray-700 mb-3">Performance Impact</h4>
              <div className="space-y-4">
                <div className="bg-green-50 p-3 rounded-lg">
                  <div className="text-sm font-medium text-green-800">Revenue Impact</div>
                  <div className="text-2xl font-bold text-green-600">+35%</div>
                  <div className="text-xs text-green-600">vs non-personalized</div>
                </div>
                <div className="bg-blue-50 p-3 rounded-lg">
                  <div className="text-sm font-medium text-blue-800">Customer Retention</div>
                  <div className="text-2xl font-bold text-blue-600">+42%</div>
                  <div className="text-xs text-blue-600">improved retention</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdvancedBusinessIntelligenceDashboard;