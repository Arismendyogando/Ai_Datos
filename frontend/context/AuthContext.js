// Suggested code may be subject to a license. Learn more: ~LicenseLog:1676117893.
// Suggested code may be subject to a license. Learn more: ~LicenseLog:263990350.
// Suggested code may be subject to a license. Learn more: ~LicenseLog:3300775249.
// Suggested code may be subject to a license. Learn more: ~LicenseLog:3286477841.
// Suggested code may be subject to a license. Learn more: ~LicenseLog:1441382565.
// Suggested code may be subject to a license. Learn more: ~LicenseLog:3033644101.

import { createContext, useContext, useEffect, useState } from 'react'
import { onAuthStateChanged } from 'firebase/auth'
import { auth } from '@/lib/firebase'

const userRoles = {
  FREELANCER
: 'freelancer',
  ACCOUNTANT: 'accountant',
  COMPANY_ADMIN: 'company_admin',
  VIRTUAL_AGENT: 'virtual_agent'
}

const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [userRole, setUserRole] = useState(null)

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setCurrentUser(user)

      setLoading(false)
    })

    return unsubscribe
  }, [])

  const value = {
    currentUser,
    loading,
    userRoles,
    userRole,
    setUserRole
  }

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
