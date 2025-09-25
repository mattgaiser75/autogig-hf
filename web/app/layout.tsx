import "./styles.css";
import Link from "next/link";

export const metadata = {
  title: "AutoGig",
  description: "Enhanced Freelance Automation Platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50 text-gray-900">
        <div className="flex">
          <aside className="w-64 min-h-screen border-r bg-white p-4 space-y-4">
            <h1 className="text-xl font-bold">AutoGig</h1>
            <nav className="space-y-2">
              <Link className="block hover:underline" href="/">Dashboard</Link>
              <Link className="block hover:underline" href="/opportunities">Opportunities</Link>
              <Link className="block hover:underline" href="/influencers">Influencers</Link>
              <Link className="block hover:underline" href="/settings">Settings</Link>
            </nav>
          </aside>
          <main className="flex-1 p-6">{children}</main>
        </div>
      </body>
    </html>
  );
}
