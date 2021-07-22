module.exports = {
  apps : [{
    name: 'microservice_sample',
    script: 'main.py',
    interpreter: 'python',

    instances: 1,
    autorestart: true,

    watch: false,

    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'development'
    },
    env_production: {
      NODE_ENV: 'production'
    }
  }]
};
