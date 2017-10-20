// Based on https://www.charted.co/embed.js

var STATS_EMBED;

(function () {
  if (STATS_EMBED && STATS_EMBED.createIframes && STATS_EMBED.onMessage) {
    STATS_EMBED.createIframes();
    return;
  }

  STATS_EMBED = {
    createIframes: function () {
      var scripts = document.getElementsByTagName('script');
      var i, statId, iframe, link;

      for (var i = 0; i < scripts.length; i++) {
        script = scripts[i];

        if (script.getAttribute('data-embed-processed')) {
          continue;
        }

        statId = script.getAttribute('data-stat');

        if (!statId) {
          continue;
        }

        iframe = document.createElement('iframe')
        iframe.setAttribute('id', 'stat-' + statId);
        iframe.setAttribute('height', '450px');
        iframe.setAttribute('width', '100%');
        iframe.setAttribute('scrolling', 'no');
        iframe.style.border = 'none';

        link = document.createElement('a');
        link.setAttribute('href', script.getAttribute('src'));
        iframe.setAttribute('src', link.origin + '/embed/' + statId);

        script.parentNode.insertBefore(iframe, script.nextSibling);
        script.setAttribute('data-embed-processed', 'yes');
      }
    }
  }

  STATS_EMBED.createIframes();
}())
