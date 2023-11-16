import { createContext, useEffect, useState } from "react";
import { checkHasApiKey, checkHasStore } from "../controllers/API";
import { storeContextType } from "../types/contexts/store";

//store context to share user components and update them
const initialValue = {
  hasStore: true,
  setHasStore: () => {},
  validApiKey: false,
  setValidApiKey: () => {},
  hasApiKey: false,
  setHasApiKey: () => {},
};

export const StoreContext = createContext<storeContextType>(initialValue);

export function StoreProvider({ children }) {
  const [hasStore, setHasStore] = useState(true);
  const [hasApiKey, setHasApiKey] = useState(false);
  const [validApiKey, setValidApiKey] = useState(false);
  const [storeChecked, setStoreChecked] = useState(false);

  useEffect(() => {
    const fetchStoreData = async () => {
      try {
        if (storeChecked) return;
        const res = await checkHasStore();
        setHasStore(res?.enabled ?? false);
        setStoreChecked(true);
      } catch (e) {
        console.log(e);
      }
    };

    fetchStoreData();
  }, []);

  useEffect(() => {
    const fetchStoreData = async () => {
      try {
        if (storeChecked) return;
        const res = await checkHasApiKey();
        console.log(res);
        setHasApiKey(res?.has_api_key ?? false);
        if (!res?.has_api_key) {
          setValidApiKey(false);
        }
      } catch (e) {
        console.log(e);
      }
    };

    fetchStoreData();
  }, [storeChecked, validApiKey]);

  return (
    <StoreContext.Provider
      value={{
        hasStore,
        setHasStore,
        hasApiKey,
        setHasApiKey,
        validApiKey,
        setValidApiKey,
      }}
    >
      {children}
    </StoreContext.Provider>
  );
}