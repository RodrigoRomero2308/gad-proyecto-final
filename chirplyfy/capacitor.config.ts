import { CapacitorConfig } from "@capacitor/cli";

const config: CapacitorConfig = {
  appId: "ar.com.rodrigoromero.chirplyfy",
  appName: "Chirplyfy",
  webDir: "dist",
  server: {
    androidScheme: "https",
  },
};

export default config;
