import React from 'react';
import { HelpCircle, Book, MessageCircle, Mail, FileText, ExternalLink } from 'lucide-react';

export const HelpSupport: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="bg-gray-800 rounded-lg border border-gray-700">
        <div className="p-4 border-b border-gray-700">
          <h2 className="text-xl font-semibold text-white">Help & Support</h2>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Documentation Section */}
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <Book className="w-5 h-5 text-blue-400" />
                <h3 className="text-lg font-medium text-white">Documentation</h3>
              </div>
              <div className="space-y-3">
                <a
                  href="#"
                  className="block p-3 bg-gray-900 rounded-lg hover:bg-gray-700 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-gray-300">Getting Started Guide</span>
                    <ExternalLink className="w-4 h-4 text-gray-400" />
                  </div>
                </a>
                <a
                  href="#"
                  className="block p-3 bg-gray-900 rounded-lg hover:bg-gray-700 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-gray-300">API Documentation</span>
                    <ExternalLink className="w-4 h-4 text-gray-400" />
                  </div>
                </a>
                <a
                  href="#"
                  className="block p-3 bg-gray-900 rounded-lg hover:bg-gray-700 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-gray-300">Security Best Practices</span>
                    <ExternalLink className="w-4 h-4 text-gray-400" />
                  </div>
                </a>
              </div>
            </div>

            {/* Contact Support Section */}
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <MessageCircle className="w-5 h-5 text-blue-400" />
                <h3 className="text-lg font-medium text-white">Contact Support</h3>
              </div>
              <div className="space-y-3">
                <button className="w-full p-3 bg-gray-900 rounded-lg hover:bg-gray-700 transition-colors flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Mail className="w-4 h-4 text-gray-400" />
                    <span className="text-gray-300">Email Support</span>
                  </div>
                  <span className="text-sm text-gray-500">24/7 Response</span>
                </button>
                <button className="w-full p-3 bg-gray-900 rounded-lg hover:bg-gray-700 transition-colors flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <MessageCircle className="w-4 h-4 text-gray-400" />
                    <span className="text-gray-300">Live Chat</span>
                  </div>
                  <span className="text-sm text-green-400">Online</span>
                </button>
              </div>
            </div>
          </div>

          {/* FAQs Section */}
          <div className="mt-8 space-y-4">
            <div className="flex items-center space-x-2">
              <HelpCircle className="w-5 h-5 text-blue-400" />
              <h3 className="text-lg font-medium text-white">Frequently Asked Questions</h3>
            </div>
            <div className="space-y-3">
              <details className="group">
                <summary className="flex items-center justify-between p-3 bg-gray-900 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors">
                  <span className="text-gray-300">How do I configure security alerts?</span>
                  <span className="text-gray-400 group-open:rotate-180 transition-transform">
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </span>
                </summary>
                <div className="mt-2 px-3 text-gray-400">
                  Navigate to Settings {'>'} Notifications to configure your security alert preferences. You can set up email, SMS, or desktop notifications for different types of security events.
                </div>
              </details>

              <details className="group">
                <summary className="flex items-center justify-between p-3 bg-gray-900 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors">
                  <span className="text-gray-300">How do I add team members?</span>
                  <span className="text-gray-400 group-open:rotate-180 transition-transform">
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </span>
                </summary>
                <div className="mt-2 px-3 text-gray-400">
                  Go to Settings {'>'} Team Access and click the "Add Team Member" button. Enter their email address and select their role to send an invitation.
                </div>
              </details>

              <details className="group">
                <summary className="flex items-center justify-between p-3 bg-gray-900 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors">
                  <span className="text-gray-300">What should I do if I detect a security breach?</span>
                  <span className="text-gray-400 group-open:rotate-180 transition-transform">
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </span>
                </summary>
                <div className="mt-2 px-3 text-gray-400">
                  Immediately isolate affected systems, document the incident, and contact our emergency response team through the Live Chat or Emergency Hotline.
                </div>
              </details>
            </div>
          </div>

          {/* Knowledge Base Quick Links */}
          <div className="mt-8">
            <div className="flex items-center space-x-2 mb-4">
              <FileText className="w-5 h-5 text-blue-400" />
              <h3 className="text-lg font-medium text-white">Knowledge Base</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <a
                href="#"
                className="p-3 bg-gray-900 rounded-lg hover:bg-gray-700 transition-colors text-gray-300 text-center"
              >
                Threat Detection
              </a>
              <a
                href="#"
                className="p-3 bg-gray-900 rounded-lg hover:bg-gray-700 transition-colors text-gray-300 text-center"
              >
                Network Security
              </a>
              <a
                href="#"
                className="p-3 bg-gray-900 rounded-lg hover:bg-gray-700 transition-colors text-gray-300 text-center"
              >
                Compliance Guides
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};