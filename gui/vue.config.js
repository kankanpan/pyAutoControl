module.exports = {
  pluginOptions: {
    electronBuilder: {
      builderOptions: {
        productName: "pyAutoControl",
        appId: "com.sample.myapplication",
        win: {
          icon: 'src/assets/app.ico',
          target: [{
            target: 'zip', // 'zip', 'nsis', 'portable'
            arch: ['x64'] // 'x64', 'ia32'
          }]
        }
      }
    }
  },
  devServer: {
    port: 8200,
    disableHostCheck: true,
  },
};
