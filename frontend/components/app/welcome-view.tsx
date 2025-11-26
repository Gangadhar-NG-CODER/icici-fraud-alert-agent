import { Button } from '@/components/livekit/button';

function WelcomeImage() {
  return (
    <div className="relative mb-8">
      <div className="absolute inset-0 bg-gradient-to-r from-blue-500 via-cyan-500 to-teal-500 rounded-full blur-2xl opacity-20 animate-pulse"></div>
      {/* Rotating ring effect */}
      <div className="absolute inset-0 rounded-full border-2 border-cyan-500/30 animate-spin" style={{ animationDuration: '8s' }}></div>
      <div className="absolute inset-2 rounded-full border-2 border-blue-500/20 animate-spin" style={{ animationDuration: '6s', animationDirection: 'reverse' }}></div>
      <svg
        width="96"
        height="96"
        viewBox="0 0 80 80"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="relative size-24 animate-bounce"
        style={{ animationDuration: '3s' }}
      >
        <circle cx="40" cy="40" r="38" fill="url(#gradient)" opacity="0.2"/>
        {/* Briefcase/Business icon */}
        <path
          d="M60 25H50V20C50 17.24 47.76 15 45 15H35C32.24 15 30 17.24 30 20V25H20C17.24 25 15 27.24 15 30V55C15 57.76 17.24 60 20 60H60C62.76 60 65 57.76 65 55V30C65 27.24 62.76 25 60 25ZM35 20H45V25H35V20ZM60 55H20V30H60V55Z"
          fill="url(#gradient)"
        />
        {/* Handshake accent */}
        <path
          d="M35 40L40 45L50 35"
          stroke="#06b6d4"
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="animate-pulse"
        />
        <defs>
          <linearGradient id="gradient" x1="0" y1="0" x2="80" y2="80">
            <stop offset="0%" stopColor="#3b82f6" />
            <stop offset="50%" stopColor="#06b6d4" />
            <stop offset="100%" stopColor="#14b8a6" />
          </linearGradient>
        </defs>
      </svg>
    </div>
  );
}

interface WelcomeViewProps {
  startButtonText: string;
  onStartCall: () => void;
}

export const WelcomeView = ({
  startButtonText,
  onStartCall,
  ref,
}: React.ComponentProps<'div'> & WelcomeViewProps) => {
  return (
    <div ref={ref} className="px-4 animate-fade-in">
      <section className="bg-background flex flex-col items-center justify-center text-center max-w-4xl mx-auto relative">
        {/* Animated background particles */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-1/4 left-1/4 w-2 h-2 bg-cyan-500/30 rounded-full animate-ping" style={{ animationDuration: '3s' }}></div>
          <div className="absolute top-1/3 right-1/4 w-2 h-2 bg-blue-500/30 rounded-full animate-ping" style={{ animationDuration: '4s', animationDelay: '1s' }}></div>
          <div className="absolute bottom-1/3 left-1/3 w-2 h-2 bg-teal-500/30 rounded-full animate-ping" style={{ animationDuration: '5s', animationDelay: '2s' }}></div>
        </div>
        <WelcomeImage />

        <h1 className="text-foreground text-4xl md:text-6xl font-bold mb-4 bg-gradient-to-r from-blue-500 via-cyan-500 to-teal-500 bg-clip-text text-transparent animate-slide-up relative">
          <span className="inline-block hover:scale-110 transition-transform duration-300">Zerodha</span>{' '}
          <span className="inline-block hover:scale-110 transition-transform duration-300">SDR</span>{' '}
          <span className="inline-block hover:scale-110 transition-transform duration-300">Agent</span>
        </h1>
        
        <p className="text-foreground/80 text-xl md:text-2xl font-medium mb-6 animate-slide-up" style={{ animationDelay: '0.1s' }}>
          AI-Powered Sales Development Representative
        </p>

        <p className="text-muted-foreground max-w-2xl text-base md:text-lg leading-relaxed mb-10 animate-slide-up" style={{ animationDelay: '0.2s' }}>
          Talk to our AI SDR to learn about Zerodha's products, pricing, and services. 
          Get your questions answered and we'll capture your information for follow-up.
        </p>

        <div className="relative group animate-slide-up" style={{ animationDelay: '0.3s' }}>
          <div className="absolute -inset-1 bg-gradient-to-r from-blue-500 via-cyan-500 to-teal-500 rounded-lg blur opacity-25 group-hover:opacity-75 transition duration-1000 group-hover:duration-200 animate-pulse"></div>
          <Button 
            variant="primary" 
            size="lg" 
            onClick={onStartCall} 
            className="relative w-72 text-lg h-14 font-semibold bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 transition-all duration-500 transform hover:scale-110 hover:shadow-2xl hover:shadow-cyan-500/50 active:scale-95"
          >
            <span className="relative z-10">{startButtonText}</span>
            <span className="absolute inset-0 rounded-lg bg-gradient-to-r from-cyan-400 to-blue-400 opacity-0 group-hover:opacity-20 transition-opacity duration-500"></span>
          </Button>
        </div>
      </section>
    </div>
  );
};
