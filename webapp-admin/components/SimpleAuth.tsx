'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { login } from '@/lib/api';

interface SimpleAuthProps {
  children: React.ReactNode;
}

const SimpleAuth: React.FC<SimpleAuthProps> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await login({ username, password });
      if (response.success && response.token) {
        localStorage.setItem('authToken', response.token);
        setIsAuthenticated(true);
      } else {
        alert(response.message || 'Invalid credentials');
      }
    } catch (error) {
      console.error('Login failed:', error);
      alert('Login failed. Please try again.');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    setIsAuthenticated(false);
    router.push('/');
  };

  if (!isAuthenticated) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-100">
        <div className="p-6 bg-white rounded shadow-md w-96">
          <h1 className="text-2xl font-bold mb-6 text-center text-gray-800">观心万象 Admin</h1>
          <form onSubmit={handleLogin}>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Username"
              className="w-full p-2 mb-4 border rounded"
            />
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              className="w-full p-2 mb-6 border rounded"
            />
            <button type="submit" className="w-full p-2 text-white bg-blue-500 rounded hover:bg-blue-600">
              Login
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div>
      {children}
      <button
        onClick={handleLogout}
        className="fixed bottom-4 right-4 px-4 py-2 text-white bg-red-500 rounded hover:bg-red-600"
      >
        Logout
      </button>
    </div>
  );
};

export default SimpleAuth;