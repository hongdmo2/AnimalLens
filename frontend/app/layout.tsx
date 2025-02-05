// Next.js의 메타데이터 타입과 폰트, 전역 스타일을 임포트
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

// Geist Sans 폰트 설정
// variable을 통해 CSS 변수로 폰트를 사용할 수 있게 함
const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

// Geist Mono 폰트 설정 (고정폭 폰트)
// 코드 표시나 특별한 텍스트에 사용
const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

// 웹사이트의 기본 메타데이터 설정
// SEO와 브라우저 탭에 표시되는 정보를 정의
export const metadata: Metadata = {
  title: "Create Next App",
  description: "Generated by create next app",
};

// 루트 레이아웃 컴포넌트
// 모든 페이지의 공통 레이아웃을 정의
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        // Geist 폰트 변수들을 적용하고 안티앨리어싱 활성화
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
