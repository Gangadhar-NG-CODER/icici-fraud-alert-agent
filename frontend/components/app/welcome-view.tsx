import { Button } from '@/components/livekit/button';

function WelcomeImage() {
  return (
    <div className="relative mb-8">
      <div className="absolute inset-0 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-full blur-2xl opacity-20 animate-pulse"></div>
      <svg
        width="96"
        height="96"
        viewBox="0 0 80 80"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="relative size-24 animate-float"
      >
        <circle cx="40" cy="40" r="38" fill="url(#gradient)" opacity="0.2"/>
        <path
          d="M40 10C23.43 10 10 23.43 10 40C10 56.57 23.43 70 40 70C56.57 70 70 56.57 70 40C70 23.43 56.57 10 40 10ZM40 20C45.52 20 50 24.48 50 30C50 35.52 45.52 40 40 40C34.48 40 30 35.52 30 30C30 24.48 34.48 20 40 20ZM40 62C32 62 24.84 58.16 20 52.2C20.16 46.04 32 42.66 40 42.66C47.96 42.66 59.84 46.04 60 52.2C55.16 58.16 48 62 40 62Z"
          fill="url(#gradient)"
        />
        <path
          d="M52 25L58 31L52 37"
          stroke="#818cf8"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="animate-pulse"
        />
        <path
          d="M28 25L22 31L28 37"
          stroke="#818cf8"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="animate-pulse"
        />
        <defs>
          <linearGradient id="gradient" x1="0" y1="0" x2="80" y2="80">
            <stop offset="0%" stopColor="#6366f1" />
            <stop offset="50%" stopColor="#a855f7" />
            <stop offset="100%" stopColor="#ec4899" />
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
      <section className="bg-background flex flex-col items-center justify-center text-center max-w-4xl mx-auto">
        <WelcomeImage />

        <h1 className="text-foreground text-4xl md:text-6xl font-bold mb-4 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent animate-slide-up">
          Teach-the-Tutor
        </h1>
        
        <p className="text-foreground/80 text-xl md:text-2xl font-medium mb-6 animate-slide-up" style={{ animationDelay: '0.1s' }}>
          Active Recall Coach
        </p>

        <p className="text-muted-foreground max-w-2xl text-base md:text-lg leading-relaxed mb-10 animate-slide-up" style={{ animationDelay: '0.2s' }}>
          Master programming concepts through active recall with AI-powered tutors. 
          Choose from Learn, Quiz, or Teach-Back modes to solidify your understanding.
        </p>

        <div className="relative group animate-slide-up" style={{ animationDelay: '0.3s' }}>
          <div className="absolute -inset-1 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 rounded-lg blur opacity-25 group-hover:opacity-75 transition duration-1000 group-hover:duration-200"></div>
          <Button 
            variant="primary" 
            size="lg" 
            onClick={onStartCall} 
            className="relative w-72 text-lg h-14 font-semibold bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105"
          >
            {startButtonText}
          </Button>
        </div>
      </section>
    </div>
  );
};
