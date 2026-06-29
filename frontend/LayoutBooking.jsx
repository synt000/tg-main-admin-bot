import React, { useState } from 'react';

export default function LayoutBooking() {
  const [selectedSlot, setSelectedSlot] = useState(null);
  
  const slots = [
    { id: 1, time: "09:00 AM - 10:00 AM", status: "Available" },
    { id: 2, time: "10:30 AM - 11:30 AM", status: "Available" },
    { id: 3, time: "01:00 PM - 02:00 PM", status: "Booked" },
    { id: 4, time: "02:30 PM - 03:30 PM", status: "Available" }
  ];

  return (
    <div className="p-2 animate-fade-in text-black">
      <h2 className="text-sm font-black mb-3">📅 ရက်ချိန်းရွေးချယ်ရန် (Time-Slot Grid)</h2>
      <div className="grid grid-cols-1 gap-3">
        {slots.map(slot => (
          <button
            key={slot.id}
            disabled={slot.status === "Booked"}
            onClick={() => setSelectedSlot(slot.id)}
            className={`w-full p-4 rounded-xl border-2 text-left flex justify-between items-center transition-all ${
              slot.status === "Booked" ? "bg-gray-100 border-gray-200 text-gray-400 cursor-not-allowed" :
              selectedSlot === slot.id ? "bg-blue-50 border-tgButton text-tgButton font-bold shadow-md" : "bg-white border-gray-200 hover:border-gray-300"
            }`}
          >
            <span className="text-xs font-bold">{slot.time}</span>
            <span className={`text-[10px] px-2 py-0.5 rounded-full font-black ${
              slot.status === "Booked" ? "bg-gray-200 text-gray-500" : "bg-emerald-100 text-emerald-600"
            }`}>{slot.status}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
