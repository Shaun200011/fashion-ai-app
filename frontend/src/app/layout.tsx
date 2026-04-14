import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Fashion AI App",
  description: "Editorial interface for garment classification and inspiration search."
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
