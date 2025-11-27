import { Button } from '@/components/livekit/button';

function WelcomeImage() {
  return (
    <div className="relative mb-8">
      {/* Animated gradient background */}
      <div className="absolute inset-0 bg-gradient-to-r from-orange-500 via-blue-500 to-orange-600 rounded-full blur-3xl opacity-30 animate-pulse" style={{ animationDuration: '4s' }}></div>
      
      {/* Multiple rotating rings */}
      <div className="absolute inset-0 rounded-full border-2 border-orange-500/40 animate-spin" style={{ animationDuration: '10s' }}></div>
      <div className="absolute inset-2 rounded-full border-2 border-blue-500/30 animate-spin" style={{ animationDuration: '7s', animationDirection: 'reverse' }}></div>
      <div className="absolute inset-4 rounded-full border border-orange-400/20 animate-spin" style={{ animationDuration: '5s' }}></div>
      
      {/* Main icon with enhanced animation */}
      <svg
        width="120"
        height="120"
        viewBox="0 0 80 80"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="relative size-28 animate-bounce"
        style={{ animationDuration: '2.5s' }}
      >
        <circle cx="40" cy="40" r="38" fill="url(#gradient)" opacity="0.15"/>
        
        {/* Shield icon for security */}
        <path
          d="M40 15L20 25V40C20 52 28 60 40 65C52 60 60 52 60 40V25L40 15Z"
          fill="url(#gradient)"
          className="drop-shadow-lg"
        />
        
        {/* Lock icon inside shield */}
        <rect x="35" y="35" width="10" height="12" rx="1" fill="#1e293b" />
        <path
          d="M37 35V32C37 30.34 38.34 29 40 29C41.66 29 43 30.34 43 32V35"
          stroke="#1e293b"
          strokeWidth="2"
          strokeLinecap="round"
        />
        
        {/* Animated alert indicator with ring */}
        <circle cx="50" cy="30" r="6" fill="#ef4444" opacity="0.2" className="animate-ping" />
        <circle cx="50" cy="30" r="4" fill="#ef4444" className="animate-pulse" />
        
        <defs>
          <linearGradient id="gradient" x1="0" y1="0" x2="80" y2="80">
            <stop offset="0%" stopColor="#f97316" />
            <stop offset="50%" stopColor="#3b82f6" />
            <stop offset="100%" stopColor="#f97316" />
          </linearGradient>
        </defs>
      </svg>
      
      {/* Floating particles */}
      <div className="absolute top-0 left-0 w-2 h-2 bg-orange-500/40 rounded-full animate-ping" style={{ animationDuration: '3s', animationDelay: '0s' }}></div>
      <div className="absolute top-4 right-2 w-1.5 h-1.5 bg-blue-500/40 rounded-full animate-ping" style={{ animationDuration: '4s', animationDelay: '1s' }}></div>
      <div className="absolute bottom-2 left-4 w-2 h-2 bg-orange-400/40 rounded-full animate-ping" style={{ animationDuration: '3.5s', animationDelay: '0.5s' }}></div>
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
        {/* Enhanced animated background particles */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-1/4 left-1/4 w-3 h-3 bg-orange-500/20 rounded-full animate-ping" style={{ animationDuration: '3s' }}></div>
          <div className="absolute top-1/3 right-1/4 w-2 h-2 bg-blue-500/20 rounded-full animate-ping" style={{ animationDuration: '4s', animationDelay: '1s' }}></div>
          <div className="absolute bottom-1/3 left-1/3 w-2.5 h-2.5 bg-orange-400/20 rounded-full animate-ping" style={{ animationDuration: '5s', animationDelay: '2s' }}></div>
          <div className="absolute top-1/2 right-1/3 w-2 h-2 bg-blue-400/20 rounded-full animate-ping" style={{ animationDuration: '4.5s', animationDelay: '0.5s' }}></div>
        </div>
        
        {/* Security Alert Badge */}
        <div className="mb-4 animate-slide-up">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-orange-500/10 border border-orange-500/30 rounded-full backdrop-blur-sm">
            <svg className="w-4 h-4 text-orange-500 animate-pulse" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <span className="text-sm font-medium text-orange-500">Fraud Alert Detected</span>
          </div>
        </div>
        
        <WelcomeImage />

        <h1 className="text-foreground text-4xl md:text-6xl font-bold mb-4 bg-gradient-to-r from-orange-500 via-blue-500 to-orange-600 bg-clip-text text-transparent animate-slide-up relative">
          <span className="inline-block hover:scale-110 transition-transform duration-300">ICICI</span>{' '}
          <span className="inline-block hover:scale-110 transition-transform duration-300">Bank</span>{' '}
          <span className="inline-block hover:scale-110 transition-transform duration-300">Fraud</span>{' '}
          <span className="inline-block hover:scale-110 transition-transform duration-300">Alert</span>
        </h1>
        
        <p className="text-foreground/80 text-xl md:text-2xl font-medium mb-6 animate-slide-up" style={{ animationDelay: '0.1s' }}>
          AI-Powered Fraud Detection Agent
        </p>

        <p className="text-muted-foreground max-w-2xl text-base md:text-lg leading-relaxed mb-10 animate-slide-up" style={{ animationDelay: '0.2s' }}>
          ICICI Bank's fraud detection system has identified a suspicious transaction on your account. 
          Connect with our AI agent to verify the transaction and protect your account.
        </p>

        <div className="relative group animate-slide-up" style={{ animationDelay: '0.3s' }}>
          {/* Animated glow effect */}
          <div className="absolute -inset-1 bg-gradient-to-r from-orange-500 via-blue-500 to-orange-600 rounded-lg blur opacity-25 group-hover:opacity-75 transition duration-1000 group-hover:duration-200 animate-pulse"></div>
          <div className="absolute -inset-2 bg-gradient-to-r from-orange-400 via-blue-400 to-orange-500 rounded-lg blur-xl opacity-0 group-hover:opacity-30 transition duration-500"></div>
          
          <Button 
            variant="primary" 
            size="lg" 
            onClick={onStartCall} 
            className="relative w-80 text-lg h-16 font-bold bg-gradient-to-r from-orange-600 via-orange-500 to-blue-600 hover:from-orange-700 hover:via-blue-600 hover:to-blue-700 transition-all duration-500 transform hover:scale-110 hover:shadow-2xl hover:shadow-orange-500/50 active:scale-95 border border-orange-400/20"
          >
            {/* Icon */}
            <svg className="w-6 h-6 mr-2 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            <span className="relative z-10">{startButtonText}</span>
            <span className="absolute inset-0 rounded-lg bg-gradient-to-r from-blue-400 to-orange-400 opacity-0 group-hover:opacity-20 transition-opacity duration-500"></span>
          </Button>
        </div>
        
        {/* Trust indicators */}
        <div className="mt-8 flex items-center gap-6 text-sm text-muted-foreground/60 animate-slide-up" style={{ animationDelay: '0.4s' }}>
          <div className="flex items-center gap-2">
            <svg className="w-4 h-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            <span>Secure Connection</span>
          </div>
          <div className="flex items-center gap-2">
            <svg className="w-4 h-4 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
              <path d="M2 5a2 2 0 012-2h7a2 2 0 012 2v4a2 2 0 01-2 2H9l-3 3v-3H4a2 2 0 01-2-2V5z" />
              <path d="M15 7v2a4 4 0 01-4 4H9.828l-1.766 1.767c.28.149.599.233.938.233h2l3 3v-3h2a2 2 0 002-2V9a2 2 0 00-2-2h-1z" />
            </svg>
            <span>AI-Powered</span>
          </div>
          <div className="flex items-center gap-2">
            <svg className="w-4 h-4 text-orange-500" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
            </svg>
            <span>24/7 Available</span>
          </div>
        </div>
      </section>
    </div>
  );
};
