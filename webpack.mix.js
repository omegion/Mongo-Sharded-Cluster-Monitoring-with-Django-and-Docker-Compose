const mix = require('laravel-mix');

mix.setPublicPath('./')
mix.disableSuccessNotifications();

mix.browserSync({
   proxy: 'localhost:100',
   open: false,
   ui: false,
   injectChanges: true,
   notify: true,
   files: [
      'mix-manifest.json',
      'app/assets/resources/**/*.*',
   ]
});

mix.js('app/assets/resources/js/app.js', 'app/assets/js')
   .sass('app/assets/resources/sass/app.scss', 'app/assets/css');