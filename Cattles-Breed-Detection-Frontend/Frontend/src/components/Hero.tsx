import heroImage from "@/assets/hero-cattle.png";

const Hero = () => {
  return (
    <section className="relative min-h-[600px] flex items-center justify-center overflow-hidden">
      <div 
        className="absolute inset-0 bg-cover bg-center"
        style={{ backgroundImage: `url(${heroImage})` }}
      >
        <div className="absolute inset-0 bg-gradient-to-r from-background/85 via-background/50 to-background/70" />
      </div>
      
      <div className="container relative z-10 px-4 py-20 mx-auto">
        <div className="max-w-3xl animate-fade-in">
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold mb-6 text-foreground">
            Cattle & Buffalo Breed Detection
          </h1>
          <p className="text-xl md:text-2xl text-muted-foreground mb-8 leading-relaxed">
            Advanced AI-powered breed identification for livestock management. Upload an image and get instant, accurate breed classification with confidence scores.
          </p>
          <div className="flex flex-wrap gap-4">
            <a href="#upload" className="inline-flex items-center justify-center rounded-md bg-primary px-8 py-4 text-lg font-semibold text-primary-foreground shadow-elegant hover:bg-primary/90 transition-all hover:scale-105">
              Start Detection
            </a>
            <a
              href="#learn-more"
              className="inline-flex items-center justify-center rounded-md border-2 border-primary bg-transparent px-8 py-4 text-lg font-semibold text-primary hover:bg-primary/10 transition-all"
            >
              Learn More
            </a>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
