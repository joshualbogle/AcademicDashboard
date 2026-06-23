import React, { createContext, useContext } from "react";

interface AuthContextValue {
	isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextValue>({ isAuthenticated: true });

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
	// For MVP we mark user as authenticated. Replace with MSAL integration later.
	return <AuthContext.Provider value={{ isAuthenticated: true }}>{children}</AuthContext.Provider>;
};

export const useAuth = () => useContext(AuthContext);
