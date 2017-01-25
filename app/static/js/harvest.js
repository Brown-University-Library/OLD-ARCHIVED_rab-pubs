var harvest = (function () {
	'use strict';

	var initModule = function ( $container ) {
		var shortid = $container.data('shortid');
		
		harvest.model.initModule();
		harvest.data.initModule( shortid );
		harvest.shell.initModule ( $container );
	};

	return { initModule: initModule };
}());
