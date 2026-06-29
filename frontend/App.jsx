
  useEffect(() => {
    if (window.Telegram && window.Telegram.WebApp) {
      const tg = window.Telegram.WebApp;
      tg.ready();
      tg.expand();
      if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
        setUser(tg.initDataUnsafe.user);
      }
      if (tg.themeParams && tg.themeParams.bg_color) {
        document.body.style.backgroundColor = tg.themeParams.bg_color;
        document.body.style.color = tg.themeParams.text_color || '#000000';
      }
    }
    const timer = setTimeout(() => setLoading(false), 2000);
    return () => clearTimeout(timer);
  }, []);

  const triggerNativeCheckout = (currentCart) => {
    if (window.Telegram && window.Telegram.WebApp) {
      const tg = window.Telegram.WebApp;
      tg.sendData(JSON.stringify({
        event: "checkout_success",
        cart: currentCart,
        total_amount: currentCart.reduce((sum, item) => sum + item.price, 0)
      }));
      tg.close();
    }
  };

  const handleAddToCart = (product) => {
    const updatedCart = [...cart, product];
    setCart(updatedCart);
    if (window.Telegram && window.Telegram.WebApp) {
      const mainBtn = window.Telegram.WebApp.MainButton;
      mainBtn.text = `Proceed to Checkout (${updatedCart.length} items)`;
      mainBtn.show();
      mainBtn.onClick(() => triggerNativeCheckout(updatedCart));
    }
  };

  return (
    <div className="min-h-screen pb-24 bg-gray-50 text-black select-none">
      <Header user={user} />
      <div className="p-4">
        {loading ? (
          <div className="grid grid-cols-2 gap-4">
            <div className="h-44 bg-gray-200 animate-pulse rounded-2xl"></div>
            <div className="h-44 bg-gray-200 animate-pulse rounded-2xl"></div>
          </div>
        ) : (
          <>
            {businessType === "ecommerce" && <LayoutEcommerce cart={cart} onAddToCart={handleAddToCart} />}
            {businessType === "booking" && <LayoutBooking />}
            {businessType === "fnb" && <LayoutFnb />}
          </>
        )}
      </div>
      <Navigation />
    </div>
  );
}
