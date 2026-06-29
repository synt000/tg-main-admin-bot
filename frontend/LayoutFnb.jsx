import React, { useState } from 'react';

export default function LayoutFnb() {
  const [activeCategory, setActiveCategory] = useState("Coffee");
  const [showPopup, setShowPopup] = useState(false);
  const categories = ["Coffee", "Tea", "Dessert", "Bakery"];

  return (
    <div className="flex gap-3 min-h-[400px] animate-fade-in text-black">
      {/* Category Sidebar */}
      <div className="w-24 bg-gray-50 border-r rounded-xl p-1 flex flex-col gap-2">
        {categories.map(cat => (
          <button
            key={cat}
            onClick={() => setActiveCategory(cat)}
            className={`py-3 text-xs font-black rounded-lg transition-all ${
              activeCategory === cat ? "bg-tgButton text-white shadow-md scale-105" : "text-gray-500 hover:bg-gray-100"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Products List Area */}
      <div className="flex-1 p-1">
        <div className="p-3 border rounded-2xl bg-white shadow-sm flex gap-3 items-center">
          <div className="w-16 h-16 bg-gray-200 rounded-xl flex items-center justify-center text-xl">☕</div>
          <div className="flex-1">
            <h3 className="text-xs font-black">Ice Americano</h3>
            <p className="text-xs text-tgLink font-bold mt-0.5">3,500 MMK</p>
            <button 
              onClick={() => setShowPopup(true)}
              className="mt-2 px-3 py-1 bg-tgButton text-white rounded-lg text-[10px] font-black"
            >
              + Customize
            </button>
          </div>
        </div>
      </div>

      {/* 🍔 ADD-ON OPTIONS POP-UP MODAL */}
      {showPopup && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50 animate-fade-in">
          <div className="bg-white rounded-2xl w-full max-w-sm p-5 shadow-2xl">
            <h3 className="font-black text-sm mb-3">☕ Ice Americano Options</h3>
            <div className="space-y-3 mb-5">
              <div>
                <p className="text-xs font-bold text-gray-500 mb-1">အချိုပမာဏ</p>
                <div className="flex gap-2">
                  <button className="px-3 py-1.5 border-2 border-tgButton text-tgButton rounded-lg text-xs font-black bg-blue-50">အချိုလျှော့</button>
                  <button className="px-3 py-1.5 border rounded-lg text-xs font-medium text-gray-600">Normal</button>
                </div>
              </div>
              <div>
                <p className="text-xs font-bold text-gray-500 mb-1">Extra Options</p>
                <label className="flex items-center gap-2 text-xs font-semibold text-gray-700">
                  <input type="checkbox" className="rounded text-tgButton" /> အပေါ်က အနှစ်ထပ်ထည့်မည် (+500 MMK)
                </label>
              </div>
            </div>
            <div className="flex gap-3">
              <button onClick={() => setShowPopup(false)} className="flex-1 py-2 bg-gray-100 text-gray-600 rounded-xl text-xs font-bold">Cancel</button>
              <button onClick={() => setShowPopup(false)} className="flex-1 py-2 bg-tgButton text-white rounded-xl text-xs font-bold">Confirm</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
