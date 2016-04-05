/* Geklaute Swipe-Funktion - Ich wollte nicht jQuery mobile benutzen,
   ist zwar an sich nützlich, macht aber Sachen kaputt wenn man es auch auf
   der Desktop-Seite benutzt und es gibt keinen verlässlichen Weg, js nur unter der Bedingung eines
   Mobilgeräts einzubinden */

/* SRC http://stackoverflow.com/questions/12428433/jquery-touch-swipe-event-no-jquery-mobile
   (modified) */

;(function($) {
  $.fn.tactile = function(swipe) {
    return this.each(function() {
      var $this = $(document),
      isTouching = false,
      start;
      $this.on('touchstart', startgesture);

      function startgesture() {
        if (event.touches.length == 1) {
          start = event.touches[0].pageX;
          isTouching = true;
          $this.on('touchmove', gesture);
        }
      }

      function endgesture() {
        $this.off('touchmove');
        isTouching = false;
        start = null;
      }

      function gesture() {
        if(isTouching) {
          var current = event.touches[0].pageX,
          delta = start - current;

          if (Math.abs(delta) >= 30) {
            if (delta > 0) {
              swipe.right();
            } else {
              swipe.left();
            }
            endgesture();
          }
        }
        event.preventDefault();
      }
    });
  };
})(jQuery);
