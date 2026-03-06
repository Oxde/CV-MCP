import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { api } from './api';

const AppContext = createContext(null);

export function AppProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Shared layout state
  const [cvs, setCvs] = useState([]);
  const [selectedCvId, setSelectedCvId] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [jobsPanelOpen, setJobsPanelOpen] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem('cv_craft_user_id');
    if (stored) {
      api.getUser(parseInt(stored))
        .then(setUser)
        .catch(() => localStorage.removeItem('cv_craft_user_id'))
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  // Load CVs when user is available
  const refreshCvs = useCallback(async () => {
    if (user) {
      const list = await api.listCVs(user.id);
      setCvs(list);
      return list;
    }
    return [];
  }, [user]);

  useEffect(() => {
    if (user?.onboarding_complete) {
      refreshCvs();
    }
  }, [user, refreshCvs]);

  const createUser = async () => {
    const u = await api.createUser();
    localStorage.setItem('cv_craft_user_id', u.id);
    setUser(u);
    return u;
  };

  const refreshUser = async () => {
    if (user) {
      const u = await api.getUser(user.id);
      setUser(u);
    }
  };

  const updateUser = async (data) => {
    if (user) {
      const u = await api.updateUser(user.id, data);
      setUser(u);
    }
  };

  const logout = () => {
    localStorage.removeItem('cv_craft_user_id');
    setUser(null);
    setCvs([]);
    setSelectedCvId(null);
  };

  return (
    <AppContext.Provider value={{
      user, loading, createUser, refreshUser, updateUser, logout,
      cvs, setCvs, selectedCvId, setSelectedCvId, refreshCvs,
      sidebarOpen, setSidebarOpen,
      jobsPanelOpen, setJobsPanelOpen,
    }}>
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  return useContext(AppContext);
}
