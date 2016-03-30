import os
import re

first_to_lowercase = lambda s: s[:1].lower() + s[1:] if s else ''
first_to_uppercase = lambda s: s[:1].upper() + s[1:] if s else ''
get_number = lambda s: filter(str.isdigit, s)

def to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def to_res(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()

def contains(sub_string, string):
	return sub_string in string

# ============================================================================================================
class ABMFile():
	def __init__(self, className, pluralName, table):
		self.code = ""
		self.class_name  = className
		self.plural_name = pluralName
		self.table = table

	def addLine(self, aLine):
		self.code += ("\n" + aLine)

	def generateCode(self):
		raise NotImplementedError("Please Implement this method")

	def execute(self):
		self.generateCode()
		os.system('touch ' + self.path)
		abm_file = open(self.path, 'w')
		abm_file.write(self.code)
		abm_file.close()

# ============================================================================================================
class ControllerFile(ABMFile):
	def __init__(self, className, pluralName):
		ABMFile.__init__(self, className, pluralName, {})
		self.path = 'backend/application/controllers/' + pluralName + 'Controller.php'

	def generateCode(self):
		code = """<?php

class MayPLURALNAMEController extends Trinomio_Rest_Controller {
	/**
 	 * @var Application_Model_MayCLASSNAME
 	 */
	protected $_model;

  public function init() {
		$this->_model = new Application_Model_MayCLASSNAME();
  }

  public function indexAction() {
  	$form = new Application_Form_MayCLASSNAMEList();
  	if ($form->isValid($this->_getAllParams())) {
			$this->view->SnakePLURALNAME = $this->_model->fetchByFilters($form->getValues())->toArray();
			$this->view->total_items = $this->_model->fetchCountByFilters($form->getValues());
		} else {
			$this->getResponse()->setHttpResponseCode(503);
			$this->view->error = $form->getMessages();
		}
	}

	public function getAction() {
		$id = $this->_getParam('id', '');
		$MinCLASSNAME = $this->_model->fetchById($id);
		if ($MinCLASSNAME) {
			$this->view->SnakeCLASSNAME = $MinCLASSNAME->toArray();
		} else {
			$this->getResponse()->setHttpResponseCode(404);
		}
	}

  public function postAction() {
		$form = new Application_Form_MayCLASSNAMEEdit();
		if ($form->isValid($this->_getAllParams())) {
			$this->view->SnakeCLASSNAME = $this->_model->insert($form->getValues())->toArray();
		} else {
			$this->view->error = $form->getMessages();
			$this->getResponse()->setHttpResponseCode(503);
		}
	}

	public function putAction() {
		$form = new Application_Form_MayCLASSNAMEEdit();
		if ($form->isValid($this->_getAllParams())) {
	  	$this->view->SnakeCLASSNAME = $this->_model->update($form->getValues())->toArray();
		} else {
			$this->getResponse()->setHttpResponseCode(503);
			$this->view->error = $form->getMessages();
		}
	}

	public function deleteAction() {
		$id = $this->_getParam('id', 0);
		$this->view->affectedRows = $this->_model->delete($id);
	}
}"""
		code = code.replace("MayCLASSNAME", self.class_name)
		code = code.replace("MinCLASSNAME", first_to_lowercase(self.class_name))
		code = code.replace("SnakeCLASSNAME", to_snake_case(self.class_name))
		code = code.replace("MayPLURALNAME", self.plural_name)
		code = code.replace("MinPLURALNAME", first_to_lowercase(self.plural_name))
		code = code.replace("SnakePLURALNAME",to_snake_case(self.plural_name))
		self.code = code

# ============================================================================================================
class ModelFile(ABMFile):
	def __init__(self, className, pluralName):
		ABMFile.__init__(self, className, pluralName, None)
		self.path = 'backend/application/models/' + className + '.php'

	def generateCode(self):
		code = """<?php
		
class Application_Model_MayCLASSNAME {
	/**
 	 * @var Application_Model_DbTable_MayCLASSNAME
 	 */
	private $_dbTable;

	public function __construct() {
		$this->_dbTable = new Application_Model_DbTable_MayCLASSNAME();
	}

	public function fetchByFilters(array $form) {
		return $this->_dbTable->fetchAll(null, "{$form['sort']} {$form['sortOrder']}", 
			$form['pageSize'], $form['pageSize'] * ($form['page'] - 1));
	}

  public function fetchCountByFilters(array $form) {
    return $this->_dbTable->fetchCount(null);
  }

	public function fetchById($id) {
		return $this->_dbTable->fetchRow(array('id = ?' => $id));
	}

	public function insert(array $data) {
		$MinCLASSNAMEId = $this->_dbTable->insert($data);
		return $this->fetchById($MinCLASSNAMEId);
 }

	public function update(array $data) {
		$this->_dbTable->update($data, array('id = ?' => $data['id']));
		return $this->fetchById($data['id']);
	}

	public function delete($id) {
		return $this->_dbTable->delete(array('id = ?' => $id));
	}
}"""
		code = code.replace("MayCLASSNAME", self.class_name)
		code = code.replace("MinCLASSNAME", first_to_lowercase(self.class_name))
		self.code = code


# ============================================================================================================
class FormListFile(ABMFile):
	def __init__(self, className, pluralName):
		ABMFile.__init__(self, className, pluralName, None)
		self.path = 'backend/application/forms/' + className + 'List.php'

	def generateCode(self):
		code = """<?php
		
class Application_Form_MayCLASSNAMEList extends Zend_Form {

	/**
 	 * @var Zend_Form_Element_Xhtml
 	 */
	public $like;
	/**
	 * @var Zend_Form_Element_Xhtml
	 */
	public $page;
	/**
	 * @var Zend_Form_Element_Xhtml
	 */
	public $pageSize;
	/**
	 * @var Zend_Form_Element_Xhtml
	 */
	public $sort;
	/**
	 * @var Zend_Form_Element_Xhtml
	 */
	public $sortOrder;

	public function init() {
		$this->setName('MayCLASSNAMEList')->setMethod('get');
		$this->like = new Zend_Form_Element_Text('like');
		$this->like->setLabel('like');
		$this->addElement($this->like);

    $this->page = new Zend_Form_Element_Text('page');
    $this->page->setLabel('page');
    $this->addElement($this->page);

    $this->pageSize = new Zend_Form_Element_Text('pageSize');
    $this->pageSize->setLabel('pageSize');
    $this->addElement($this->pageSize);

    $this->sort = new Zend_Form_Element_Text('sort');
    $this->sort->setLabel('sort');
    $this->addElement($this->sort);

    $this->sortOrder = new Zend_Form_Element_Text('sortOrder');
    $this->sortOrder->setLabel('sortOrder');
    $this->addElement($this->sortOrder);
	}
}"""
		code = code.replace("MayCLASSNAME", self.class_name)
		self.code = code

# ============================================================================================================
class FormEditFile(ABMFile):
	def __init__(self, className, pluralName, table):
		ABMFile.__init__(self, className, pluralName, table)
		self.path = 'backend/application/forms/' + className + 'Edit.php'

	def generateCode(self):
		table_name = first_to_lowercase(self.plural_name)
		self.addLine("<?php")
		self.addLine("")
		self.addLine("class Application_Form_" + self.class_name + "Edit extends Zend_Form {")
		self.addLine("")
		self.declareVariables()
		self.addLine("")
		self.addLine("	public function init() {")
		self.addLine("		$this->setName('" + self.class_name + "Edit')->setMethod('post');")
		self.defineVariables()
		self.addLine("	}")
		self.addLine("}")

	def declareVariables(self):
		for key in self.table.keys():
			self.addLine("	/**")
			self.addLine("	 * @var Zend_Form_Element_Xhtml")
			self.addLine("	*/")
			self.addLine("	public $" + key + ";")

	def defineVariables(self):
		for key in self.table.keys():
			self.addLine("		$this->" + key + " = new Zend_Form_Element_Text('" + key + "');")
			self.addLine("		$this->" + key + "->setLabel('" + first_to_uppercase(key) + "');")
			fiel_type = self.table[key]
			if contains('varchar', fiel_type):
				len_field = get_number(fiel_type)
				self.addLine("		$this->" + key + "->addValidator('stringLength', false, array(0, " + len_field + "));")

			if key != 'id':
				self.addLine("		$this->" + key + "->setRequired(true);")
	
			self.addLine("		$this->addElement($this->" + key + ");")
			self.addLine("")

# ============================================================================================================
class DBTableFile(ABMFile):
	def __init__(self, className, pluralName, table):
		ABMFile.__init__(self, className, pluralName, table)
		self.path = 'backend/application/models/DbTable/' + className + '.php'

	def generateCode(self):
		self.code += "<?php\n\n/**"
		self.generateTable()
		code = """
*/
class Application_Model_DbTable_MayCLASSNAME extends Trinomio_DbTable_Abstract {

	protected $_name = 'SnakePLURALNAME';

}"""
		code = code.replace("MayCLASSNAME", self.class_name)
		code = code.replace("SnakePLURALNAME",to_snake_case(self.plural_name))
		self.code += code

	def generateTable(self):
		self.addLine("create table " + to_snake_case(self.plural_name) + " (")
		for key in self.table.keys():
			self.addLine("	" + key + " " + self.table[key] + ",")
		self.addLine("	primary key (id)")
		self.addLine(");")

# ============================================================================================================
class ServiceFile(ABMFile):
	def __init__(self, className, pluralName):
		ABMFile.__init__(self, className, pluralName, None)
		self.path = 'frontend/app/scripts/services/' + first_to_lowercase(pluralName) + '.js'

	def generateCode(self):
		MinCLASSNAME  = first_to_lowercase(self.class_name)
		MinPLURALNAME = first_to_lowercase(self.plural_name)
		self.addLine("var speakersFrontApp = angular.module('speakersFrontApp');")
		self.addLine("")
		self.addLine("(function() {")
		self.addLine("")
		self.addLine("	'use strict';")
		self.addLine("")
		self.addLine("	/**")
		self.addLine("	 * @ngdoc function")
		self.addLine("	 * @name speakersFrontApp.factory:" + MinPLURALNAME + "Service")
		self.addLine("	 * @description")
		self.addLine("	 * # " + MinPLURALNAME + "Service")
		self.addLine("	 * Factory of the speakersFrontApp")
		self.addLine("	 */")
		self.addLine("	speakersFrontApp.factory('" + MinPLURALNAME + "Service', function(dbConnectedService, api2URL) {")
		self.addLine("		var instance = {")
		self.addLine("			serviceName: '" + to_res(self.plural_name) + "',")
		self.addLine("			uriToPut: function(" + MinCLASSNAME + ") {")
		self.addLine("				return this.serviceName + '/' + " + MinCLASSNAME + ".id;")
		self.addLine("			},")
		self.addLine("			url: api2URL")
		self.addLine("		};")
		self.addLine("		return angular.extend(angular.copy(dbConnectedService), instance);")
		self.addLine("	});")
		self.addLine("})();")

# ============================================================================================================
class EditControllerFile(ABMFile):
	def __init__(self, className, pluralName):
		ABMFile.__init__(self, className, pluralName, None)
		self.path = 'frontend/app/scripts/controllers/' + first_to_lowercase(pluralName) + 'Edit.js'

	def generateCode(self):
		code = """var speakersFrontApp = angular.module('speakersFrontApp');

(function() {

	'use strict';

	/**
	 * @ngdoc function
	 * @name speakersFrontApp.controller:MayPLURALNAMEEditCtrl
	 * @description
	 * # MayPLURALNAMEEditCtrl
	 * Controller of the speakersFrontApp
	*/
	speakersFrontApp.controller('MayPLURALNAMEEditCtrl', function ($scope, MinPLURALNAMEService, data) {
		/* Controller definitions */
		$scope.data = {
			MinCLASSNAME : data.SnakeCLASSNAME,
			isNew: !('id' in data.SnakeCLASSNAME)
		};

		$scope.backToList = function(){
			window.location = '#/UrlPLURALNAME';
		};

		$scope.saveMayCLASSNAME = function(form){
			if (form.$valid) {
				MinPLURALNAMEService.save($scope.data.MinCLASSNAME, $scope.data.isNew).then(function(){
					window.location = '#/UrlPLURALNAME';
				});
			}
		};
	});
	
	speakersFrontApp.resolveMayPLURALNAMEEditCtrl = {
		data: function($route, MinPLURALNAMEService) {
			if ($route.current.params.id && $route.current.params.id.length > 0) {
				return MinPLURALNAMEService.fetchOne($route.current.params.id);
			} else {
				return { SnakeCLASSNAME: { } };
			}
		}
	};
})();"""
		code = code.replace('MayCLASSNAME' , self.class_name)
		code = code.replace('MinCLASSNAME' , first_to_lowercase(self.class_name))
		code = code.replace('MayPLURALNAME' , self.plural_name)
		code = code.replace('MinPLURALNAME' , first_to_lowercase(self.plural_name))
		code = code.replace('SnakeCLASSNAME' , to_snake_case(self.class_name))
		code = code.replace('MinTotalPLURALNAME' , self.plural_name.lower())
		code = code.replace('UrlPLURALNAME' , to_res(self.plural_name))
		self.code = code


# ============================================================================================================
class ListControllerFile(ABMFile):
	def __init__(self, className, pluralName):
		ABMFile.__init__(self, className, pluralName, None)
		self.path = 'frontend/app/scripts/controllers/' + first_to_lowercase(pluralName) + 'List.js'

	def generateCode(self):
		code = """var speakersFrontApp = angular.module('speakersFrontApp');

(function() {

	'use strict';

	/**
	 * @ngdoc function
	 * @name speakersFrontApp.controller:MayPLURALNAMEListCtrl
	 * @description
	 * # MayPLURALNAMEListCtrl
	 * Controller of the speakersFrontApp
	 */
	speakersFrontApp.controller('MayPLURALNAMEListCtrl', function ($scope, $controller, MinPLURALNAMEService, MinPLURALNAMETable) {
		angular.extend(this, $controller('AbstractDbConnectedCtrl', { 
			$scope : $scope,
			currentService : MinPLURALNAMEService,
			currentTable : MinPLURALNAMETable,
			currentUrl : 'UrlPLURALNAME',
			deleteResolve: {
        title: function() {
          return 'Delete MayCLASSNAME';
        },
        message: function() {
          return 'Are you sure you want delete this MayCLASSNAME?'
        }
      }
		}));
	});
	
	speakersFrontApp.resolveMayPLURALNAMEListCtrl = {
		MinPLURALNAMETable: function($q, ngTableParams, MinPLURALNAMEService, tableService) {
			return tableService.createNgTableResolve($q, ngTableParams, function(count, page, sorting) {
				return MinPLURALNAMEService.fetchAll(count, page, sorting);
			}, {
				page: 1,
				count: 10,
				sorting: {
					id: 'asc'
				}
			}, function(data) {
				return data.SnakePLURALNAME;
			}
			);
		}
	};
})();"""
		code = code.replace('MayCLASSNAME', self.class_name)
		code = code.replace('MayPLURALNAME', self.plural_name)
		code = code.replace('MinPLURALNAME', first_to_lowercase(self.plural_name))
		code = code.replace('UrlPLURALNAME', to_res(self.plural_name))
		code = code.replace('SnakePLURALNAME', to_snake_case(self.plural_name))
		self.code = code

# ============================================================================================================
class ListHtmlFile(ABMFile):
	def __init__(self, className, pluralName, table):
		ABMFile.__init__(self, className, pluralName, table)
		self.path = 'frontend/app/views/' + to_res(pluralName) + '-list.html'

	def generateCode(self):
		MinCLASSNAME  = first_to_lowercase(self.class_name)
		MayPLURALNAME = self.plural_name
		MinPLURALNAME = first_to_lowercase(self.plural_name)
		self.addLine('<div class="row">')
		self.addLine('  <div class="col-xs-9">')
		self.addLine('    <h1 style="margin-top:10px">' + self.class_name.upper() + '</h1>')
		self.addLine('	</div>')
		self.addLine('	<div class="col-xs-3">')
		self.addLine('		<div class="well">')
		self.addLine('			<button type="button" class="btn btn-default" ng-click="newItem()">')
		self.addLine('				<span class="glyphicon glyphicon-plus"></span> New ' + self.class_name)
		self.addLine('			</button>')
		self.addLine('		</div>')
		self.addLine('	</div>')
		self.addLine('</div> ')
		self.addLine('')
		self.generateTable()

	def generateTable(self):
		MinCLASSNAME  = first_to_lowercase(self.class_name)
		UrlPLURALNAME = to_res(self.plural_name)
		self.addLine('<table ng-table="table" class="table table-hover">')
		self.addLine('	<tr ng-repeat="' + MinCLASSNAME + ' in $data">')
		for key in self.table.keys():
			self.addLine('		<td data-title="' + "'" + first_to_uppercase(key) + "'" + '" sortable="'+ "'" + key + "'" + '">')
			self.addLine('			<div ng-bind="' + MinCLASSNAME + '.' + key + '"/>')
			self.addLine('		</td>')
		self.addLine('		<td style="width: 25%;">')
		self.addLine('			<a class="btn" href="#/' + UrlPLURALNAME + '/edit/{{' + MinCLASSNAME + '.id}}"><span class="glyphicon glyphicon-pencil"/></a>')
		self.addLine('			<a class="btn"ng-click="deleteItem(' + MinCLASSNAME + '.id)">   <span class="glyphicon glyphicon-trash"/></a>')
		self.addLine('		</td>')
		self.addLine('	</tr>')
		self.addLine('</table>')

# ============================================================================================================
class EditHtmlFile(ABMFile):
	def __init__(self, className, pluralName, table):
		ABMFile.__init__(self, className, pluralName, table)
		self.path = 'frontend/app/views/' + to_res(pluralName) + '-edit.html'

	def generateCode(self):
		self.addLine('<div class="row">')
		self.addLine('  <div class="container">')
		self.addLine('    <div class="col-xs-12">')
		self.addLine('      <h1 class="center">' + self.class_name.upper() + '</h1>')
		self.addLine('    </div>')
		self.addLine('  </div>')
		self.addLine('</div>')
		self.addLine('<form name="form" class="main-form" novalidate ng-submit="save' + self.class_name + '(form)">')
		self.generateFields()
		self.addLine('	<button type="submit" class="btn btn-primary"> Save ' + self.class_name + ' </button>')
		self.addLine('	<button type="button" class="btn btn-default" ng-click="backToList()"> Back to List </button>')
		self.addLine('</form>')

	def generateFields(self):
		MinCLASSNAME  = first_to_lowercase(self.class_name)
		MinPLURALNAME = first_to_lowercase(self.plural_name)
		for key in self.table.keys():
			if key != 'id':
				fiel_type  = self.table[key]
				input_text = '		<input type="text" name="' + key + '" class="form-control" ng-model="data.' + MinCLASSNAME + '.' + key + '" placeholder="' + first_to_uppercase(key) + '"'
				
				if contains('varchar', fiel_type):
					input_text += ' required maxlength="' + get_number(fiel_type) + '" />'
				else:
					input_text += ' required/>'

				self.addLine('	<div class="form-group">')
				self.addLine('		<label> ' + first_to_uppercase(key) + ' </label>')
				self.addLine(input_text)
				self.addLine('		<span class="error-message" ng-show="form.$submitted && form.' + key + '.$error.required">This field is required</span>')
				self.addLine('	</div>')

# ============================================================================================================
class ABMCreator(object):
	def __init__(self, className, pluralName, table):
		self.class_name  = className
		self.plural_name = pluralName
		self.files = []
		self.table = table
		self.initialize()

	def initialize(self):
		# Backend
		self.files.append(ModelFile(self.class_name, self.plural_name))
		self.files.append(DBTableFile(self.class_name, self.plural_name, self.table))
		self.files.append(FormListFile(self.class_name, self.plural_name))
		self.files.append(FormEditFile(self.class_name, self.plural_name, self.table))
		self.files.append(ControllerFile(self.class_name, self.plural_name))
		# Frontend
		self.files.append(ServiceFile(self.class_name, self.plural_name))
		self.files.append(EditControllerFile(self.class_name, self.plural_name))
		self.files.append(ListControllerFile(self.class_name, self.plural_name))
		self.files.append(ListHtmlFile(self.class_name, self.plural_name, self.table))
		self.files.append(EditHtmlFile(self.class_name, self.plural_name, self.table))

	def execute(self):
		for abm_file in self.files:
			abm_file.execute()
			print("generated " + abm_file.path)

		MayPLURALNAME = self.plural_name
		MinPLURALNAME = first_to_lowercase(self.plural_name)
		ResPLURALNAME = to_res(self.plural_name)
		UrlPLURALNAME = to_res(self.plural_name)
		print("")
		print(".when('/" + UrlPLURALNAME + "',{")
		print("	 templateUrl: 'views/" + ResPLURALNAME + "-list.html',")
		print("	 controller : '" + MayPLURALNAME + "ListCtrl',")
		print("  resolve: speakersFrontApp.resolve" + MayPLURALNAME + "ListCtrl,")
		print("}).when('/" + UrlPLURALNAME + "/edit/:id',{")
		print("  templateUrl: 'views/" + ResPLURALNAME + "-edit.html',")
		print("  controller : '" + MayPLURALNAME + "EditCtrl',")
		print("  resolve: speakersFrontApp.resolve" + MayPLURALNAME + "EditCtrl")
		print("}).when('/" + UrlPLURALNAME + "/new',{")
		print("	 templateUrl: 'views/" + ResPLURALNAME + "-edit.html',")
		print("  controller : '" + MayPLURALNAME + "EditCtrl',")
		print("	 resolve: speakersFrontApp.resolve" + MayPLURALNAME + "EditCtrl")
		print("})")
		print("")
		print('<li ng-class="getNavSidebarClassItem(' + "'/" + UrlPLURALNAME + "')" + '"' + '><a ng-href="#/' + UrlPLURALNAME + '">' + self.plural_name + '</a></li>')
		print("")
		print('<script src="scripts/services/' + MinPLURALNAME + '.js"></script>')
		print("")
		print('<script src="scripts/controllers/' + MinPLURALNAME + 'List.js"></script>')
		print("")
		print('<script src="scripts/controllers/' + MinPLURALNAME + 'Edit.js"></script>')

# ============================================================================================================

car_agencies = {}
car_agencies['id']     = 'integer not null auto_increment'
car_agencies['name']   = 'varchar(50)'
car_agencies['cityId'] = 'integer'
car_agencies['address']= 'varchar(200)'
car_agencies['phone']  = 'varchar(50)'
car_agencies['fax']    = 'varchar(50)'
car_agencies['email']  = 'varchar(50)'
car_agencies['web']    = 'varchar(50)'
car_agencies['mobile'] = 'varchar(100)'
carAgencie = ABMCreator('CarAgencie', 'CarAgencies', car_agencies)

sponsors = {}
sponsors['id']     = 'integer not null auto_increment'
sponsors['name']   = 'varchar(100)'
sponsors['description'] = 'varchar(500)'
sponsor = ABMCreator('Sponsor', 'Sponsors', sponsors)

airlines = {}
airlines['id']     = 'integer not null auto_increment'
airlines['name']   = 'varchar(50)'
airline = ABMCreator('Airline', 'Airlines', airlines)

cities = {}
cities['id']     = 'integer not null auto_increment'
cities['name']   = 'varchar(50)'
cities['countryCode'] = 'varchar(3)'
city = ABMCreator('City', 'Cities', cities)

venues = {}
venues['id']       = 'integer not null auto_increment'
venues['name']     = 'varchar(50)'
venues['address']  = 'varchar(200)'
venues['phone']    = 'varchar(50)'
venues['fax']      = 'varchar(50)'
venues['email']    = 'varchar(50)'
venues['web']      = 'varchar(50)'
venues['capacity'] = 'integer'
venues['cityId']   = 'integer'
venue = ABMCreator('Venue', 'Venues', venues)

subeventTypes = {}
subeventTypes['id']    = 'integer not null auto_increment'
subeventTypes['name']  = 'varchar(50)'
subeventTypes['color'] = 'varchar(7)'
subeventType = ABMCreator('EventSubeventType', 'EventSubeventTypes', subeventTypes)

subeventFormats = {}
subeventFormats['id']    = 'integer not null auto_increment'
subeventFormats['name']  = 'varchar(50)'
subeventFormats['eventItemTypeId'] = 'integer'
subeventFormat = ABMCreator('EventSubeventFormat', 'EventSubeventFormats', subeventFormats)

moderatorRoles = {}
moderatorRoles['id']    = 'integer not null auto_increment'
moderatorRoles['name']  = 'varchar(50)'
moderatorRole = ABMCreator('ModeratorRole', 'ModeratorRoles', moderatorRoles)

contractStatuses = {}
contractStatuses['id']    = 'integer not null auto_increment'
contractStatuses['name']  = 'varchar(50)'
contractStatuses['color']  = 'varchar(7)'
contractStatus = ABMCreator('ContractStatus', 'ContractStatuses', contractStatuses)

attachmentTypes = {}
attachmentTypes['id']    = 'integer not null auto_increment'
attachmentTypes['name']  = 'varchar(100)'
attachmentTypes['origin'] = "enum('contracts','events','subevents','speakers')"
attachmentType = ABMCreator('AttachmentType', 'AttachmentTypes', attachmentTypes)

hotels = {}
hotels['id']      = 'integer not null auto_increment'
hotels['name']    = 'varchar(100)'
hotels['cityId']  = 'integer'
hotels['address'] = 'varchar(200)'
hotels['phone']   = 'varchar(50)'
hotels['mobile']  = 'varchar(50)'
hotels['fax']     = 'varchar(50)'
hotels['email']   = 'varchar(200)'
hotels['web']     = 'varchar(50)'
hotel = ABMCreator('Hotel', 'Hotels', hotels)

# =========================================================================================================
# SUBEVENT
subevents = {}
subevents['id']            =  'integer not null auto_increment'
subevents['eventId']       =  'integer'
subevents['eventTypeId']   =  'integer'
subevents['eventFormatId'] =  'integer'
subevents['name']          =  'varchar(50)'
subevents['startDate']     =  'timestamp'
subevents['endDate']       =  'timestamp'
subevents['location']      =  'varchar(100)'
subevents['mediaOutlet']   =  'varchar(50)'
subevents['audienceProfile'] =  'text'
subevents['expectedAttendees'] =  'integer'
subevent = ABMCreator('Subevent', 'Subevents', subevents)

# =========================================================================================================
subeventAttachments = {}
subeventAttachments['id']           =  'integer not null auto_increment'
subeventAttachments['subeventId']   = 'integer'
subeventAttachments['attachmentId'] = 'integer'
subeventAttachments['onStage']      = 'bit(1)'
subeventAttachment = ABMCreator('SubeventAttachment', 'SubeventAttachments', subeventAttachments)

subeventBooks = {}
subeventBooks['id'] = 'integer not null auto_increment'
subeventBooks['subeventId'] = 'integer'
subeventBooks['name'] = 'varchar(255)'
subeventBooks['isbn'] = 'integer(13)'
subeventBooks['genre'] = 'varchar(50)'
subeventBook = ABMCreator('SubeventBook', 'SubeventBooks', subeventBooks)

subeventContacts = {}
subeventContacts['id'] = 'integer not null auto_increment'
subeventContacts['subeventId'] = 'integer'
subeventContacts['contactId']  = 'integer'
subeventContacts['isMain']     = 'bit(1)'
subeventContact = ABMCreator('SubeventContact', 'SubeventContacts', subeventContacts)

subeventModerators = {}
subeventModerators['id'] = 'integer not null auto_increment'
subeventModerators['subeventId'] = 'integer'
subeventModerators['moderatorId'] = 'integer'
subeventModerator = ABMCreator('SubeventModerator', 'SubeventModerators', subeventModerators)

subeventSpeakers = {}
subeventSpeakers['id'] = 'integer not null auto_increment'
subeventSpeakers['subeventId'] = 'integer'
subeventSpeakers['speakerId']  = 'integer'
subeventSpeaker = ABMCreator('SubeventSpeaker', 'SubeventSpeakers', subeventSpeakers)

subeventSponsors = {}
subeventSponsors['id'] = 'integer not null auto_increment'
subeventSponsors['subeventId']   = 'integer'
subeventSponsors['sponsorId']    = 'integer'
subeventSponsors['expectations'] = 'text'
subeventSponsor = ABMCreator('SubeventSponsor', 'SubeventSponsors', subeventSponsors)

# subevent.execute()
# subeventAttachment.execute()
# subeventBook.execute()
# subeventContact.execute()
# subeventModerator.execute()
# subeventSpeaker.execute()
# subeventSponsor.execute()

# =========================================================================================================

speakerLogistics = {}
speakerLogistics['id'] = 'integer not null auto_increment'
speakerLogistics['eventId'] = 'integer'
speakerLogistics['speakerId'] = 'integer'
speakerLogistics['fromDate'] = 'timestamp'
speakerLogistics['toDate'] = 'timestamp'
speakerLogistics['currencyCode'] = 'integer'
speakerLogistics['price'] = 'numeric(10,2)'
speakerLogistics['type'] = "enum('transfer', 'hotel', 'flight')"
speakerLogistic = ABMCreator('SpeakerLogistics', 'SpeakerLogistics', speakerLogistics)
speakerLogistic.execute()


"""
create table events_logistics
	id integer not null auto_increment,
	eventId integer,
	speakerId integer,
	fromDate timestamp,
	toDate timestamp,
	currencyCode integer,
	price numeric(10,2),
	type enum('transfer', 'hotel', 'flight'),
	primary key (id)
);

create table events_transfers ( 
	id integer not null,
	eventCompanionId integer,
	carAgencyId integer,
	pickupAddress varchar(200),
	destinationAddress varchar(200),
	description text,
	primary key (id)
);

create table events_transfers_contacts (
	id integer not null auto_increment,
	eventTransferId integer,
	contactId integer,
	primary key (id)
);

create table events_hotel_bookings (
	id integer not null,
  hotelId integer,
  eventCompanionId integer,
  roomType varchar(50),
  bookedBy enum('wobi', 'bureau', 'speaker'),
  primary key (id)
);

create table events_flights (
	id integer not null,
	airlineId integer,
	code varchar(7),
	class varchar(50),
	departureAirportCode integer,
	departureTransferId integer,
	arribalAirportCode integer,
	arrivalTransferId integer,
	backupFligths varchar(50),
	primary key (id)
);
"""