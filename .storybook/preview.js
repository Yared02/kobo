import 'jsapp/scss/main.scss';
import 'js/bemComponents';

export const parameters = {
  actions: {argTypesRegex: '^on[A-Z].*'},
  controls: {
    matchers: {
      color: /(background|color)$/i,
      date: /Date$/,
    },
  },
};

window.t = function (str) {
  return str;
};
