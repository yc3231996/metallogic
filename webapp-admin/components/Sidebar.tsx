'use client';

import React, { useState } from 'react';
import Link from "next/link";
import { usePathname } from 'next/navigation';
import {
  Home,
  FolderOpen,
  Brain,
  Menu,
  X
} from "lucide-react";

const menuItems = [
  { icon: Home, label: 'Home', href: '/' },
  { icon: FolderOpen, label: 'Workspace管理', href: '/workspace-management' },
  { icon: Brain, label: 'Workspace建模', href: '/modeling' },
];

const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const pathname = usePathname();

  const toggleSidebar = () => setIsOpen(!isOpen);

  return (
    <>
      <button
        className="lg:hidden fixed top-4 left-4 z-20"
        onClick={toggleSidebar}
      >
        {isOpen ? <X /> : <Menu />}
      </button>
      <aside className={`w-64 h-screen bg-gray-100 flex flex-col fixed lg:static transition-all duration-300 ease-in-out ${isOpen ? 'left-0' : '-left-64'} lg:left-0`}>
        <div className="p-4 border-b border-gray-200 text-center">
          <h1 className="text-xl font-bold text-blue-600">观心万象-Admin</h1>
        </div>
        <nav className="flex-grow py-4">
          {menuItems.map((item, index) => (
            <Link
              key={index}
              href={item.href}
              className={`flex items-center px-4 py-3 text-gray-700 hover:bg-gray-200 ${pathname === item.href ? 'bg-gray-200' : ''}`}
            >
              <item.icon className="h-5 w-5 mr-3" />
              <span className="text-base">{item.label}</span>
            </Link>
          ))}
        </nav>
      </aside>
    </>
  );
};

export default Sidebar;