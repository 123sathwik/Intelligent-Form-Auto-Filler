import React from 'react'
import { Outlet, Link, useLocation } from 'react-router-dom'
import { LayoutDashboard, FileText, Settings, LogOut, Menu } from 'lucide-react'

export default function DashboardLayout() {
  const location = useLocation()

  const navigation = [
    { name: 'Dashboard', href: '/', icon: LayoutDashboard },
    { name: 'Upload Document', href: '/upload', icon: FileText },
    { name: 'Settings', href: '/settings', icon: Settings },
  ]

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 overflow-hidden">
      {/* Sidebar Desktop */}
      <div className="hidden md:flex md:w-64 md:flex-col bg-slate-900 border-r border-slate-800">
        <div className="flex flex-col flex-grow pt-5 pb-4 overflow-y-auto">
          {/* Logo container */}
          <div className="flex items-center flex-shrink-0 px-4 mb-8">
            <span className="text-lg font-black tracking-tight bg-gradient-to-r from-brand-400 to-indigo-300 bg-clip-text text-transparent">
              AutoFiller AI
            </span>
          </div>
          {/* Navigation Links */}
          <nav className="mt-5 flex-1 px-2 space-y-1">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href
              const Icon = item.icon
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`group flex items-center px-3 py-2.5 text-sm font-semibold rounded-xl transition-all duration-200 ${
                    isActive
                      ? 'bg-brand-600 text-white shadow-lg shadow-brand-500/20'
                      : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
                  }`}
                >
                  <Icon
                    className={`mr-3 flex-shrink-0 h-5 w-5 transition-transform group-hover:scale-105`}
                  />
                  {item.name}
                </Link>
              )
            })}
          </nav>
        </div>
        {/* User profile / Logout placeholder */}
        <div className="flex-shrink-0 flex border-t border-slate-800 p-4">
          <button className="w-full group flex items-center px-3 py-2 text-sm font-semibold text-slate-400 hover:text-rose-400 rounded-xl hover:bg-slate-800 transition-colors">
            <LogOut className="mr-3 h-5 w-5" />
            Sign Out
          </button>
        </div>
      </div>

      {/* Main content area */}
      <div className="flex flex-col flex-1 overflow-hidden">
        {/* Mobile Header */}
        <header className="flex items-center justify-between px-4 py-3 md:hidden bg-slate-900 border-b border-slate-800">
          <span className="text-md font-bold tracking-tight bg-gradient-to-r from-brand-400 to-indigo-300 bg-clip-text text-transparent">
            AutoFiller AI
          </span>
          <button className="p-2 text-slate-400 hover:text-slate-200">
            <Menu size={20} />
          </button>
        </header>

        {/* Dynamic page content */}
        <main className="flex-1 relative overflow-y-auto focus:outline-none p-6 bg-slate-950">
          <div className="max-w-7xl mx-auto">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  )
}
