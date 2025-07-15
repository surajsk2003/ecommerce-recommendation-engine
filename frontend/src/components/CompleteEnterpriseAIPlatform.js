import React, { useState } from 'react';
import { 
  BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, 
  Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import { 
  TrendingUp, DollarSign, Users, Globe, Cpu, Shield, Package, 
  Building, BarChart3, CheckCircle, Award, Eye, Settings, 
  Palette, Sliders
} from 'lucide-react';

const CompleteEnterpriseAIPlatform = () => {
  const [currentView, setCurrentView] = useState('dashboard');
  const [selectedClient, setSelectedClient] = useState('demo-client');

  const whitelabelClients = {
    'demo-client': {
      name: 'Demo Store', domain: 'demo.smartcommerce.ai',
      theme: { primaryColor: '#667eea', logo: '🛍️' },
      features: ['recommendations', 'analytics', 'voice'],
      metrics: { revenue: 2847500, users: 127543, conversion: 0.078, satisfaction: 4.6 }
    },
    'fashion-boutique': {
      name: 'Fashion Boutique Pro', domain: 'boutique.fashionai.com',
      theme: { primaryColor: '#ff6b9d', logo: '👗' },
      features: ['recommendations', 'analytics', 'ar'],
      metrics: { revenue: 1234000, users: 45000, conversion: 0.092, satisfaction: 4.8 }
    },
    'tech-electronics': {
      name: 'TechMart AI', domain: 'tech.smartcommerce.ai',
      theme: { primaryColor: '#00d4aa', logo: '💻' },
      features: ['recommendations', 'voice', 'specs-ai'],
      metrics: { revenue: 3456000, users: 89000, conversion: 0.065, satisfaction: 4.4 }
    }
  };

  const enterpriseFeatures = {
    ai_capabilities: [
      { name: 'Collaborative Filtering', performance: 91.7 },
      { name: 'Deep Learning', performance: 89.4 },
      { name: 'Computer Vision', performance: 85.6 },
      { name: 'NLP Processing', performance: 92.1 }
    ],
    integrations: [
      { name: 'Shopify', clients: 245 },
      { name: 'WooCommerce', clients: 189 },
      { name: 'Magento', clients: 156 },
      { name: 'Custom API', clients: 567 }
    ],
    security: [
      { feature: 'End-to-End Encryption', status: 'enabled', level: 'AES-256' },
      { feature: 'GDPR Compliance', status: 'certified', level: 'Full' },
      { feature: 'SOC 2 Type II', status: 'certified', level: 'Annual' },
      { feature: 'ISO 27001', status: 'certified', level: 'Current' }
    ]
  };

  const globalDeployment = {
    regions: [
      { name: 'North America', clients: 1247, revenue: 45600000, growth: 34.5 },
      { name: 'Europe', clients: 892, revenue: 32400000, growth: 28.7 },
      { name: 'Asia Pacific', clients: 678, revenue: 28900000, growth: 52.1 }
    ],
    infrastructure: { uptime: 99.97, requests_per_second: 2340000 }
  };

  const businessImpact = {
    roi_metrics: [
      { metric: 'Revenue Increase', average: 35.7, best: 89.2, industry: 'Fashion' },
      { metric: 'Conversion Rate Boost', average: 28.4, best: 67.8, industry: 'Electronics' },
      { metric: 'Customer Retention', average: 42.1, best: 78.9, industry: 'Home & Garden' }
    ]
  };

  const DashboardView = () => (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-blue-600 to-purple-700 rounded-xl p-6 text-white">
        <div className="flex justify-between items-start">
          <div>
            <h2 className="text-2xl font-bold mb-2">SmartCommerce AI Platform</h2>
            <p className="text-blue-100">Enterprise-grade AI recommendation engine</p>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold">
              ${(Object.values(whitelabelClients).reduce((sum, client) => sum + client.metrics.revenue, 0) / 1000000).toFixed(1)}M
            </div>
            <div className="text-blue-100">Total Revenue</div>
          </div>
        </div>
        
        <div className="grid grid-cols-4 gap-4 mt-6">
          <div className="bg-white bg-opacity-20 rounded-lg p-3">
            <div className="text-2xl font-bold">
              {Object.values(whitelabelClients).reduce((sum, client) => sum + client.metrics.users, 0).toLocaleString()}
            </div>
            <div className="text-sm text-blue-100">Total Users</div>
          </div>
          <div className="bg-white bg-opacity-20 rounded-lg p-3">
            <div className="text-2xl font-bold">
              {globalDeployment.regions.reduce((sum, region) => sum + region.clients, 0).toLocaleString()}
            </div>
            <div className="text-sm text-blue-100">Active Clients</div>
          </div>
          <div className="bg-white bg-opacity-20 rounded-lg p-3">
            <div className="text-2xl font-bold">{globalDeployment.infrastructure.requests_per_second.toLocaleString()}</div>
            <div className="text-sm text-blue-100">Requests/Second</div>
          </div>
          <div className="bg-white bg-opacity-20 rounded-lg p-3">
            <div className="text-2xl font-bold">{globalDeployment.infrastructure.uptime}%</div>
            <div className="text-sm text-blue-100">Uptime</div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
          <Cpu className="w-6 h-6 mr-2 text-blue-500" />
          AI Capabilities Performance
        </h3>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {enterpriseFeatures.ai_capabilities.map((capability, index) => (
            <div key={index} className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <div className="w-3 h-3 rounded-full bg-green-500"></div>
                <span className="text-sm font-medium text-gray-600">{capability.performance}%</span>
              </div>
              <h4 className="font-medium text-sm text-gray-800">{capability.name}</h4>
              <div className="mt-2 bg-gray-200 rounded-full h-2">
                <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${capability.performance}%` }}></div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
            <Globe className="w-6 h-6 mr-2 text-green-500" />
            Global Deployment
          </h3>
          <div className="space-y-4">
            {globalDeployment.regions.map((region, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <div className="font-medium text-gray-800">{region.name}</div>
                  <div className="text-sm text-gray-600">{region.clients} clients</div>
                </div>
                <div className="text-right">
                  <div className="font-bold text-green-600">${(region.revenue / 1000000).toFixed(1)}M</div>
                  <div className="text-sm text-green-600">+{region.growth}%</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
            <TrendingUp className="w-6 h-6 mr-2 text-purple-500" />
            Business Impact
          </h3>
          <div className="space-y-4">
            {businessImpact.roi_metrics.map((metric, index) => (
              <div key={index} className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="font-medium text-gray-800">{metric.metric}</div>
                  <div className="text-sm text-gray-600">Best: +{metric.best}% ({metric.industry})</div>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-blue-600">+{metric.average}%</div>
                  <div className="text-xs text-gray-500">Average</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  const WhiteLabelView = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-800">White-Label Client Management</h2>
        <button className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 flex items-center">
          <Package className="w-4 h-4 mr-2" />
          Deploy New Client
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {Object.entries(whitelabelClients).map(([clientId, client]) => (
          <div 
            key={clientId} 
            className={`bg-white rounded-xl shadow-lg p-6 cursor-pointer transition-all ${
              selectedClient === clientId ? 'ring-2 ring-blue-500' : 'hover:shadow-xl'
            }`}
            onClick={() => setSelectedClient(clientId)}
          >
            <div className="flex items-center justify-between mb-4">
              <div className="text-3xl">{client.theme.logo}</div>
              <div className="w-3 h-3 rounded-full bg-green-500"></div>
            </div>
            <h3 className="font-bold text-lg text-gray-800 mb-1">{client.name}</h3>
            <p className="text-sm text-gray-600 mb-4">{client.domain}</p>
            
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Revenue</span>
                <span className="font-medium">${(client.metrics.revenue / 1000).toFixed(0)}K</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Users</span>
                <span className="font-medium">{client.metrics.users.toLocaleString()}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Conversion</span>
                <span className="font-medium">{(client.metrics.conversion * 100).toFixed(1)}%</span>
              </div>
            </div>
            
            <div className="mt-4 flex flex-wrap gap-1">
              {client.features.map((feature, index) => (
                <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                  {feature}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>

      {selectedClient && (
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center">
              <div className="text-4xl mr-4">{whitelabelClients[selectedClient].theme.logo}</div>
              <div>
                <h3 className="text-xl font-bold text-gray-800">{whitelabelClients[selectedClient].name}</h3>
                <p className="text-gray-600">{whitelabelClients[selectedClient].domain}</p>
              </div>
            </div>
            <div className="flex space-x-2">
              <button className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600 flex items-center">
                <Settings className="w-4 h-4 mr-2" />
                Configure
              </button>
              <button className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 flex items-center">
                <Eye className="w-4 h-4 mr-2" />
                Preview
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div>
              <h4 className="font-bold text-gray-800 mb-3 flex items-center">
                <Palette className="w-5 h-5 mr-2" />
                Theme
              </h4>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Primary Color</label>
                  <div className="flex items-center space-x-2">
                    <div 
                      className="w-8 h-8 rounded border"
                      style={{ backgroundColor: whitelabelClients[selectedClient].theme.primaryColor }}
                    ></div>
                    <span className="text-sm font-mono">{whitelabelClients[selectedClient].theme.primaryColor}</span>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <h4 className="font-bold text-gray-800 mb-3 flex items-center">
                <Sliders className="w-5 h-5 mr-2" />
                Features
              </h4>
              <div className="space-y-2">
                {whitelabelClients[selectedClient].features.map((feature, index) => (
                  <div key={index} className="flex items-center justify-between">
                    <span className="text-sm text-gray-700 capitalize">{feature.replace('-', ' ')}</span>
                    <div className="w-10 h-6 rounded-full p-1 bg-green-500">
                      <div className="w-4 h-4 rounded-full bg-white translate-x-4"></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h4 className="font-bold text-gray-800 mb-3 flex items-center">
                <BarChart3 className="w-5 h-5 mr-2" />
                Metrics
              </h4>
              <div className="space-y-3">
                <div className="bg-gray-50 p-3 rounded-lg">
                  <div className="text-sm text-gray-600">Revenue</div>
                  <div className="text-2xl font-bold text-green-600">
                    ${(whitelabelClients[selectedClient].metrics.revenue / 1000).toFixed(0)}K
                  </div>
                </div>
                <div className="bg-gray-50 p-3 rounded-lg">
                  <div className="text-sm text-gray-600">Users</div>
                  <div className="text-2xl font-bold text-blue-600">
                    {whitelabelClients[selectedClient].metrics.users.toLocaleString()}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );

  const SecurityView = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-800 flex items-center">
          <Shield className="w-7 h-7 mr-3 text-blue-500" />
          Security & Compliance
        </h2>
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 bg-green-500 rounded-full"></div>
          <span className="text-sm font-medium text-green-600">All Systems Secure</span>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4">Security Features</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {enterpriseFeatures.security.map((feature, index) => (
            <div key={index} className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center">
                  <CheckCircle className="w-5 h-5 text-green-500 mr-2" />
                  <span className="font-medium text-gray-800">{feature.feature}</span>
                </div>
                <span className="px-2 py-1 rounded text-xs font-medium bg-green-100 text-green-800">
                  {feature.status}
                </span>
              </div>
              <div className="text-sm text-gray-600">Level: {feature.level}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4">Compliance Certifications</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg">
            <div className="flex items-center">
              <Award className="w-6 h-6 text-green-600 mr-3" />
              <div>
                <div className="font-medium text-gray-800">SOC 2 Type II</div>
                <div className="text-sm text-gray-600">Security & Availability</div>
              </div>
            </div>
            <div className="text-sm text-green-600 font-medium">Valid until Dec 2024</div>
          </div>
          
          <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
            <div className="flex items-center">
              <Award className="w-6 h-6 text-blue-600 mr-3" />
              <div>
                <div className="font-medium text-gray-800">ISO 27001</div>
                <div className="text-sm text-gray-600">Information Security</div>
              </div>
            </div>
            <div className="text-sm text-blue-600 font-medium">Valid until Mar 2025</div>
          </div>
        </div>
      </div>
    </div>
  );

  const navigation = [
    { id: 'dashboard', label: 'Platform Overview', icon: BarChart3 },
    { id: 'whitelabel', label: 'White-Label Clients', icon: Building },
    { id: 'security', label: 'Security & Compliance', icon: Shield }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Cpu className="w-8 h-8 text-blue-500 mr-3" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">SmartCommerce AI</h1>
                <p className="text-xs text-gray-500">Enterprise Platform</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <span className="text-sm text-gray-600">All Systems Operational</span>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex space-x-1 mb-8 bg-gray-100 rounded-lg p-1">
          {navigation.map((item) => (
            <button
              key={item.id}
              onClick={() => setCurrentView(item.id)}
              className={`flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                currentView === item.id
                  ? 'bg-white text-blue-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <item.icon className="w-4 h-4 mr-2" />
              {item.label}
            </button>
          ))}
        </div>

        <div className="transition-all duration-300">
          {currentView === 'dashboard' && <DashboardView />}
          {currentView === 'whitelabel' && <WhiteLabelView />}
          {currentView === 'security' && <SecurityView />}
        </div>
      </div>
    </div>
  );
};

export default CompleteEnterpriseAIPlatform;