export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold">Citas App MVP</h1>
        <p className="text-gray-600 mt-4">Appointment Management System</p>
        
        <div className="mt-8 grid grid-cols-2 gap-4">
          <div className="p-4 border rounded-lg">
            <h2 className="text-lg font-semibold">Admin Login</h2>
            <p className="text-sm text-gray-600">Manage appointments and availability</p>
          </div>
          <div className="p-4 border rounded-lg">
            <h2 className="text-lg font-semibold">Client Services</h2>
            <p className="text-sm text-gray-600">Book your appointment</p>
          </div>
        </div>
      </div>
    </main>
  )
}
