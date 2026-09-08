import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "LibraryOS",
  description: "Discover and organize books from digital libraries.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
