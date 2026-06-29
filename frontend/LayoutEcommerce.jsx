import React from 'react';

export default function LayoutEcommerce({ cart, onAddToCart }) {
  // စမ်းသပ်ရန် Sample Products
  const products = [
    { id: 101, name: "Premium Smart Digital Account", price: 15000, img: "https://unsplash.com" },
    { id: 102, name: "Enterprise Whitelabel Token", price: 35000, img: "https://unsplash.com" }
  ];

  return (
    <div className="grid grid-cols-2 gap-4 animate-fade-in">
      {products.map(product => (
        <div key={product.id} className="p-3 border rounded-2xl bg-white shadow-sm flex flex-col justify-between text-black">
          <img 
            src={product.img} 
            alt={product.name} 
            loading="lazy" 
            className="w-full h-28 object-cover rounded-xl transition-opacity duration-300" 
          />
          <div className="mt-2">
            <h3 className="text-xs font-black leading-tight line-clamp-2">{product.name}</h3>
            <p className="text-xs text-tgLink font-black mt-1">{product.price.toLocaleString()} MMK</p>
          </div>
          
          {/* CTA Button */}
          <button 
            onClick={() => onAddToCart(product)}
            className="mt-3 w-full py-2 bg-emerald-500 text-white rounded-xl text-xs font-bold active:scale-95 transition-all shadow-sm shadow-emerald-200"
          >
            Add to Cart
          </button>
        </div>
      ))}
    </div>
  );
}
