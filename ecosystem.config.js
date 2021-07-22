module.exports = {
  apps : [{
    name: 'skinzu_core',
    script: 'main.py',
    interpreter: 'python',

    // Options reference: https://pm2.keymetrics.io/docs/usage/application-declaration/
    //args: 'one two',
    instances: 1,
    autorestart: true,

    watch: true,
    // watch_options: {
    //   usePolling: true
    //   followSymlinks: false,
    //   persistent    : true,
    //   ignoreInitial : true
    // },

    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'development'
    },
    env_production: {
      NODE_ENV: 'production'
    }
  }]
};
