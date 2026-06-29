import React from 'react';

export default function Navigation() {
  return (
    <div className="fixed bottom-0 left-0 right-0 h-16 bg-white/90 backdrop-blur-md border-t flex items-center justify-around pb-safe z-50 text-black shadow-lg">
      <button className="flex flex-col items-center gap-0.5 text-tgButton font-bold">
        <span className="text-lg">🏠</span>
        <span className="text-[10px]">Home</span>
      </button>
      <button className="flex flex-col items-center gap-0.5 text-gray-400 font-medium">
        <span className="text-lg">🔍</span>
        <span className="text-[10px]">Explore</span>
      </button>
      <button className="flex flex-col items-center gap-0.5 text-gray-400 font-medium">
        <span className="text-lg">📦</span>
        <span className="text-[10px]">My Orders</span>
      </button>
      <button className="flex flex-col items-center gap-0.5 text-gray-400 font-medium">
        <span className="text-lg">👤</span>
        <span className="text-[10px]">Profile</span>
      </button>
    </div>
  );
}
