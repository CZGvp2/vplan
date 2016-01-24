void setup() {
  size(displayWidth, displayHeight);
  noCursor();
  
  PFont mono;
  mono = createFont("Consolas", 50);
  textFont(mono, 50);
}

void draw() {
  background(0);
  timer();
}
