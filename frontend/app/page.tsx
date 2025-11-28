import Image from "next/image";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <Image
        src="/image.png"
        alt="Tarjman Logo"
        width={150}
        height={150}
        className="mb-8"
      />
     
    </main>
  );
}
