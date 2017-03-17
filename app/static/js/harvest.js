var harvest = (function () {
	'use strict';

	var initModule = function ( $container, config ) {		
		harvest.model.initModule( config.sources );

		harvest.data.configModule( config );
		harvest.data.initModule();
		harvest.shell.initModule ( $container );
	};

	return { initModule: initModule };
}());
