import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Sidebar from "../components/Sidebar";
import SimpleAuth from "../components/SimpleAuth";
import "./globals.css";
import { Toaster } from "@/components/ui/toaster";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "观心万象-ADMIN",
  description: "后台管理",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <SimpleAuth>
          <div className="flex h-screen">
            <Sidebar />
            <main className="flex-1 overflow-auto p-4">
              {children}
            </main>
          </div>
          <Toaster />
        </SimpleAuth>
      </body>
    </html>
  );
}