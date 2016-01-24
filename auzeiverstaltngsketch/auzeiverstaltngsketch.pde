int mode; // Modus für die einzelnen Abschnitte

final int TIMER = 0;

void setup() {
  size(displayWidth, displayHeight);
  noCursor();
  
  PFont mono;
  mono = createFont("Consolas", 50);
  textFont(mono, 50);
  
  setMode(TIMER);
}

void draw() {
  background(0);
  
  tick();
  switch (mode) {
   case TIMER: timer(); break;
  }
}

void keyPressed() {
  if ("0123456789".indexOf(key) > -1) setMode(key-48);
  if (key == 'p') togglePaused();
}

void setMode(int x) {
  mode = x;
}
