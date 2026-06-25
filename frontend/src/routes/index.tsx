import React, { lazy } from 'react'
import { createBrowserRouter } from 'react-router-dom'
import DashboardLayout from '@/layouts/DashboardLayout'
import ErrorPage from '@/pages/common/ErrorPage'
import NotFoundPage from '@/pages/common/NotFoundPage'

// Simple placeholder page components (to keep routes modular but compiling)
const Dashboard = lazy(() => import('@/pages/Dashboard'))
const Upload = lazy(() => import('@/pages/Upload'))
const Settings = lazy(() => import('@/pages/Settings'))
const FormReview = lazy(() => import('@/pages/FormReview'))

export const router = createBrowserRouter([
  {
    path: '/',
    element: <DashboardLayout />,
    errorElement: <ErrorPage />,
    children: [
      {
        index: true,
        element: <Dashboard />,
      },
      {
        path: 'upload',
        element: <Upload />,
      },
      {
        path: 'settings',
        element: <Settings />,
      },
      {
        path: 'review',
        element: <FormReview />,
      },
    ],
  },
  {
    path: '*',
    element: <NotFoundPage />,
  },
])
