import React from 'react';
import Link from "next/link";
import {
  Home,
  FolderOpen,
  Brain,
  Settings,
} from "lucide-react";

const menuItems = [
  { icon: FolderOpen, label: 'Workspace管理', href: '/workspace-management' },
  { icon: Brain, label: 'Workspace建模', href: '/workspace-modeling' },
];

const Sidebar = () => {
  return (
    <aside className="w-64 h-screen bg-gray-100 flex flex-col">
      <div className="p-4 border-b border-gray-200 text-center">
        <h1 className="text-xl font-bold text-blue-600">观心万象-Admin</h1>
        <p className="text-sm text-gray-600"></p>
      </div>
      <nav className="flex-grow py-4">
        {menuItems.map((item, index) => (
          <Link
            key={index}
            href={item.href}
            className="flex items-center px-4 py-3 text-gray-700 hover:bg-gray-200"
          >
            <item.icon className="h-5 w-5 mr-3" />
            <span className="text-base">{item.label}</span>
          </Link>
        ))}
      </nav>
      <div className="border-t border-gray-200">
        <Link href="/settings" className="flex items-center px-4 py-3 text-gray-700 hover:bg-gray-200">
          <Settings className="h-5 w-5 mr-3" />
          <span className="text-base">设置</span>
        </Link>
      </div>
    </aside>
  );
};

const HomePage: React.FC = () => {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 p-4">
        <h1 className="text-2xl font-bold mb-4">Playground 测试页面</h1>
        <p>这是使用新布局的测试内容。您可以在这里添加更多的组件或内容来测试布局的效果。</p>
      </main>
    </div>
  );
};

export default HomePage;