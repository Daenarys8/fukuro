import React from 'react';
import { Save, Bell, Shield, Lock, Users, Database } from 'lucide-react';

export const Settings: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="bg-gray-800 rounded-lg border border-gray-700">
        <div className="p-4 border-b border-gray-700">
          <h2 className="text-xl font-semibold text-white">Security Settings</h2>
        </div>
        <div className="p-6 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Notification Settings */}
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <Bell className="w-5 h-5 text-blue-400" />
                <h3 className="text-lg font-medium text-white">Notifications</h3>
              </div>
              <div className="space-y-3">
                <label className="flex items-center space-x-3">
                  <input type="checkbox" className="form-checkbox text-blue-500" defaultChecked />
                  <span className="text-gray-300">Email Alerts</span>
                </label>
                <label className="flex items-center space-x-3">
                  <input type="checkbox" className="form-checkbox text-blue-500" defaultChecked />
                  <span className="text-gray-300">SMS Notifications</span>
                </label>
                <label className="flex items-center space-x-3">
                  <input type="checkbox" className="form-checkbox text-blue-500" defaultChecked />
                  <span className="text-gray-300">Desktop Notifications</span>
                </label>
              </div>
            </div>

            {/* Security Thresholds */}
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <Shield className="w-5 h-5 text-blue-400" />
                <h3 className="text-lg font-medium text-white">Security Thresholds</h3>
              </div>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">
                    Failed Login Attempts
                  </label>
                  <input
                    type="number"
                    className="bg-gray-700 text-white rounded-md px-3 py-2 w-full"
                    defaultValue={3}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">
                    Session Timeout (minutes)
                  </label>
                  <input
                    type="number"
                    className="bg-gray-700 text-white rounded-md px-3 py-2 w-full"
                    defaultValue={30}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* API Access */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <Lock className="w-5 h-5 text-blue-400" />
              <h3 className="text-lg font-medium text-white">API Access</h3>
            </div>
            <div className="bg-gray-900 p-4 rounded-lg">
              <div className="flex items-center justify-between mb-4">
                <span className="text-gray-300">API Key</span>
                <button className="text-blue-400 hover:text-blue-300 text-sm">
                  Generate New Key
                </button>
              </div>
              <input
                type="text"
                className="bg-gray-700 text-white rounded-md px-3 py-2 w-full font-mono"
                value="sk_test_123456789"
                readOnly
              />
            </div>
          </div>

          {/* Team Access */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <Users className="w-5 h-5 text-blue-400" />
              <h3 className="text-lg font-medium text-white">Team Access</h3>
            </div>
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 bg-gray-900 rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                    <span className="text-white font-medium">JD</span>
                  </div>
                  <div>
                    <div className="text-white">John Doe</div>
                    <div className="text-sm text-gray-400">Admin</div>
                  </div>
                </div>
                <button className="text-red-400 hover:text-red-300 text-sm">
                  Remove
                </button>
              </div>
              <button className="text-blue-400 hover:text-blue-300 text-sm">
                + Add Team Member
              </button>
            </div>
          </div>

          {/* Backup Settings */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <Database className="w-5 h-5 text-blue-400" />
              <h3 className="text-lg font-medium text-white">Backup Settings</h3>
            </div>
            <div className="space-y-3">
              <label className="flex items-center space-x-3">
                <input type="checkbox" className="form-checkbox text-blue-500" defaultChecked />
                <span className="text-gray-300">Enable Automatic Backups</span>
              </label>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  Backup Frequency
                </label>
                <select className="bg-gray-700 text-white rounded-md px-3 py-2 w-full">
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                </select>
              </div>
            </div>
          </div>

          <div className="flex justify-end pt-4">
            <button className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center space-x-2">
              <Save className="w-4 h-4" />
              <span>Save Settings</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};