import re, config_parser


# =============================
# Congifs
# ============================================================================================================

config = config_parser.getConfigTree('ibox_scaffolder.cfg')


# =============================
# Helper Functions
# ============================================================================================================

firstToLowercase = lambda s: s[:1].lower() + s[1:] if s else ''
firstToUppercase = lambda s: s[:1].upper() + s[1:] if s else ''
getNumber = lambda s: filter(str.isdigit, s)

def foldS(func, l):
    if not l:
        return ""
    else:
        return func(l[0]) + foldS(func, l[1:])

def toSnakeCase(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def toRes(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()

def contains(sub_string, string):
    return sub_string in string

def replaceAllTokens(text, tokens):
    for token, replacement in tokens.iteritems():
        if replacement:
            text = text.replace('{{{' + token + '}}}', replacement)
        else:
            text = text.replace('{{{' + token + '}}}\n', '')
            text = text.replace('{{{' + token + '}}}', '')
    return text

def getPhpKeyArrayFromDict(dic, indent):
    return "array(\n" + indent*2 + (",\n" + indent*2).join(["'" + k + "' => " + v for k, v in dic.items()]) + "\n" + indent + ")"


# =============================
# Abstract Classes
# ============================================================================================================

class ABMFile():
    def __init__(self, className, pluralName, templateName):
        self.templateName = config['metadata']['templates'] + templateName + '.' + config['metadata']['extension']
        self.class_name  = className
        self.plural_name = pluralName
        self.templateTokens = {
            'upper_name'        : self.class_name,
            'lower_name'        : firstToLowercase(self.class_name),
            'snake_name'        : toSnakeCase(self.class_name),
            'upper_plural_name' : self.plural_name,
            'lower_plural_name' : firstToLowercase(self.plural_name),
            'snake_plural_name' : toSnakeCase(self.plural_name)
        }

    def generateCode(self):
        with open(self.templateName) as templateFile:
            template = templateFile.read()
            self.code = replaceAllTokens(template, self.templateTokens)

    def execute(self):
        self.generateCode()
        with open(self.path, 'w') as abmFile:
            abmFile.write(self.code)
        print("- GENERATED: " + self.path)

class ABMFormFile(ABMFile):
    def __init__(self, className, pluralName, templateName, properties):
        ABMFile.__init__(self, className, pluralName, templateName)
        self.addPropertiesTokens(properties)

    def addPropertiesTokens(self, properties):
        formVariables = ""
        formElements = ""
        for prop in properties.keys():
            formVariables += "    /**\n"
            formVariables += "     * @var Zend_Form_Element_Xhtml\n"
            formVariables += "     */\n"
            formVariables += "    public $" + prop + ";\n"
        
            formElements += "        $this->" + prop + " = new Zend_Form_Element_Text('" + prop + "');\n"
            formElements += "        $this->" + prop + "->setLabel('" + prop + "');\n"
            formElements += "        $this->addElement($this->" + prop + ");\n\n"

        self.templateTokens['form_variables'] = formVariables
        self.templateTokens['form_elements'] = formElements
        

# =============================
# Backend Controller
# ============================================================================================================

class ControllerFile(ABMFile):
    def __init__(self, className, pluralName, foreignProperties):
        ABMFile.__init__(self, className, pluralName, 'backend_controller')
        self.path = config['backend']['controllers'] + pluralName + 'Controller.php'
        self.addEditFormTokens(foreignProperties);

    def addEditFormTokens(self, abms):
        countVariables     = ""
        formEditParameters = ""
        for abm in abms:
            countVariables     += self.countVariables(abm)
            formEditParameters += self.constructorParams(abm)
        formEditParameters = formEditParameters[:-1]
        formEditParameters = formEditParameters[:-1]

        self.templateTokens['count_variables']      = countVariables
        self.templateTokens['form_edit_parameters'] = formEditParameters 

    def constructorParams(self, abm):
        return "$numberOf" + abm.plural_name + ", " + foldS(self.constructorParams, abm.foreignProperties)

    def countVariables(self, prop):
        abm = prop.files[0]
        return "    $numberOf" + abm.plural_name + " = count($this->_getParam('" + abm.templateTokens['lower_plural_name'] + "'));\n" + foldS(self.countVariables, prop.foreignProperties)

# =============================
# Backend Model
# ============================================================================================================

class ModelFile(ABMFile):
    def __init__(self, className, pluralName, foreignProperties, expansions):
        ABMFile.__init__(self, className, pluralName, 'backend_model')
        self.path = config['backend']['models'] + className + '.php'
        self.addForeignTokens(foreignProperties, expansions)

    def addForeignTokens(self, foreignProperties, expansions):
        foreignDbtablesDeclarations = ""
        foreignDbtablesInstantiations = ""
        foreignUnsets = ""
        foreignInserts = ""
        foreignUpdates = ""

        singleExpansionsMap = expansions['single'] if 'single' in expansions else {}
        listExpansionsMap = expansions['list'] if 'list' in expansions else {}

        for prop in foreignProperties:
            abm = prop.files[0]
            upperName = abm.templateTokens['upper_name']
            lowerName = abm.templateTokens['lower_name']
            lowerPluralName = abm.templateTokens['lower_plural_name']

            pk = singleExpansionsMap[lowerName]['pk'] if lowerName in singleExpansionsMap else listExpansionsMap[lowerName]['pk']
            pk = firstToUppercase(pk)
            
            foreignDbtablesDeclarations += "  /**\n"
            foreignDbtablesDeclarations += "   * @var Teleperformance_Model_DbTable_" + upperName + "\n"
            foreignDbtablesDeclarations += "   */\n"
            foreignDbtablesDeclarations += "  private $_" + lowerName + "DbTable;\n\n"

            foreignDbtablesInstantiations += "    $this->_" + lowerName + "DbTable = "
            foreignDbtablesInstantiations += "new Teleperformance_Model_DbTable_" + upperName + "();\n"

            foreignUnsets += "    $" + lowerPluralName + " = $data['" + lowerPluralName + "'];\n"
            foreignUnsets += "    unset($data['" + lowerPluralName + "']);\n\n"

            foreignInserts += "    $this->saveRelated($this->_" + lowerName + "DbTable, '"
            foreignInserts += self.templateTokens['lower_name'] + pk + "', $id, $" + lowerPluralName + ");\n"

            foreignUpdates += "    $this->saveRelated($this->_" + lowerName + "DbTable, '"
            foreignUpdates += self.templateTokens['lower_name'] + pk + "', $data['id'], $" + lowerPluralName + ");\n"

        self.templateTokens['foreign_dbtables_declarations'] = foreignDbtablesDeclarations
        self.templateTokens['foreign_dbtables_instantiations'] = foreignDbtablesInstantiations
        self.templateTokens['foreign_unsets'] = foreignUnsets
        self.templateTokens['foreign_inserts'] = foreignInserts
        self.templateTokens['foreign_updates'] = foreignUpdates


# =============================
# Backend Dto
# ============================================================================================================

class DtoFile(ABMFile):
    def __init__(self, className, pluralName, properties, foreignProperties, expansions):
        ABMFile.__init__(self, className, pluralName, 'backend_dto')
        self.path = config['backend']['dtos'] + className + '.php'
        self.addPropertiesTokens(properties)
        self.addForeignPropertiesTokens(foreignProperties)
        self.addExpansions(properties, foreignProperties, expansions)

    def addPropertiesTokens(self, properties):
        propertiesDeclarations = ""
        propertiesSet = ""

        for prop in properties.keys():
            propertiesDeclarations += "    public $" + prop + ";\n"

            propertiesSet += "        $this->" + prop + " = $" + self.templateTokens['lower_name'] + "Row->" + prop + ";\n"

        self.templateTokens['properties_declarations'] = propertiesDeclarations
        self.templateTokens['properties_set'] = propertiesSet

    def getDbTableDeclaration(self, dbTableLowerName):
        dbTableName = firstToUppercase(dbTableLowerName)

        text = "    /**\n"
        text += "     * @var Teleperformance_Model_DbTable_" + dbTableName + "\n"
        text += "     */\n"
        text += "    private static $" + dbTableLowerName + "DbTable;\n\n"

        text += "    private function get" + dbTableName + "DbTable() {\n"
        text += "        if (!self::$" + dbTableLowerName + "DbTable) {\n"
        text += "            self::$" + dbTableLowerName + "DbTable = new Teleperformance_Model_DbTable_" + dbTableName + "();\n"
        text += "        }\n"
        text += "        return self::$" + dbTableLowerName + "DbTable;\n"
        text += "    }\n\n"

        return text

    def addForeignPropertiesTokens(self, foreignProperties):
        foreignDtosDeclarations = ""
        #foreignDbtablesSet = ""
        #foreignDtosSet = ""

        #selfLowerName = self.templateTokens['lower_name']
        for prop in foreignProperties:
            abm = prop.files[0]
            className = abm.class_name
            #lowerName = abm.templateTokens['lower_name']
            #lowerPluralName = abm.templateTokens['lower_plural_name']

            foreignDtosDeclarations += "    /**\n"
            foreignDtosDeclarations += "     * @var array Teleperformance_Model_Dto_" + className + "\n"
            foreignDtosDeclarations += "     */\n"
            foreignDtosDeclarations += "    public $" + abm.templateTokens['lower_plural_name'] + ";\n\n"


            # foreignDbtablesSet += "        $this->" + abm.templateTokens['lower_name'] + "DbTable"
            # foreignDbtablesSet += " = new Teleperformance_Model_DbTable_" + className + "();\n"

            # foreignDtosSet += "        $" + lowerName + "Rows = $this->" + lowerName + "DbTable->fetchAll("
            # foreignDtosSet += "array('" + selfLowerName + "_id = ?' => $" + selfLowerName + "Row->id));\n"
            # foreignDtosSet += "        $this->" + lowerPluralName + " = array();\n"
            # foreignDtosSet += "        foreach ($" + lowerName + "Rows as $" + lowerName + "Row) {\n"
            # foreignDtosSet += "            array_push($this->" + lowerPluralName + ", "
            # foreignDtosSet += "new Teleperformance_Model_Dto_" + className + "($" + lowerName + "Row));\n"
            # foreignDtosSet += "        }\n\n"

        self.templateTokens['foreign_dtos_declarations'] = foreignDtosDeclarations
        #self.templateTokens['foreign_dbtables_set'] = foreignDbtablesSet
        #self.templateTokens['foreign_dtos_set'] = foreignDtosSet

    def getSingleExpandText(self, prop, info):
        dbTableName = firstToUppercase(info['dbtable'])
        dtoName   = "Teleperformance_Model_Dto_" + dbTableName
        dtoReturn = "$this->get" + dbTableName + "DbTable()->fetchByPk($this->" + prop + ", '" + info['pk'] + "')"
        return "        $this->" + info['dbtable'] + " = new " + dtoName + "(" + dtoReturn + ");\n\n"
        
    def getListExpandText(self, abm, info):
        dbTableName = firstToUppercase(info['dbtable'] if 'dbtable' in info else abm.class_name)
        lowerName = abm.templateTokens['lower_name']
        lowerPluralName = abm.templateTokens['lower_plural_name']
        selfLowerName = self.templateTokens['lower_name']
                
        text =  "        $" + lowerName + "Rows = $this->get" + dbTableName + "DbTable()->fetchAll("
        text += "array('" + selfLowerName + firstToUppercase(info['pk']) + " = ?' => $this->id));\n"
        text += "        $this->" + lowerPluralName + " = array();\n"
        text += "        foreach ($" + lowerName + "Rows as $" + lowerName + "Row) {\n"
        text += "            array_push($this->" + lowerPluralName + ", "
        text += "new Teleperformance_Model_Dto_" + dbTableName + "($" + lowerName + "Row));\n"
        text += "        }\n\n"

        return text

    def addExpansions(self, properties, foreignProperties, expansions):
        dbTablesDeclarations = ""
        singleExpansions = ""
        listExpansions = ""

        singleExpansionsMap = expansions['single'] if 'single' in expansions else {}
        listExpansionsMap = expansions['list'] if 'list' in expansions else {}

        for prop in properties:
            if prop in singleExpansionsMap:
                dbTablesDeclarations += self.getDbTableDeclaration(singleExpansionsMap[prop]['dbtable'])
                singleExpansions += self.getSingleExpandText(prop, singleExpansionsMap[prop])
            elif prop in listExpansionsMap:
                dbTablesDeclarations += self.getDbTableDeclaration(listExpansionsMap[prop]['dbtable'])
                listExpansions += self.getSingleExpandText(prop, listExpansionsMap[prop])

        for prop in foreignProperties:
            if prop.files:
                abm = prop.files[0]
                lowerName = abm.templateTokens['lower_name']
                if lowerName in singleExpansionsMap:
                    dbTablesDeclarations += self.getDbTableDeclaration(singleExpansionsMap[lowerName]['dbtable'])
                    singleExpansions += self.getListExpandText(abm, singleExpansionsMap[lowerName])
                elif lowerName in listExpansionsMap:
                    dbTablesDeclarations += self.getDbTableDeclaration()
                    listExpansions += self.getListExpandText(abm, listExpansionsMap[lowerName])

        self.templateTokens['single_expansions'] = singleExpansions
        self.templateTokens['list_expansions'] = listExpansions
        self.templateTokens['dbtables_declarations'] = dbTablesDeclarations


# =============================
# Backend List Form
# ============================================================================================================

class FormListFile(ABMFormFile):
    def __init__(self, className, pluralName, properties):
        ABMFormFile.__init__(self, className, pluralName, 'backend_list_form', properties)
        self.path = config['backend']['forms'] + pluralName + 'List.php'


# =============================
# Backend Edit Form
# ============================================================================================================

class FormEditFile(ABMFormFile):
    def __init__(self, className, pluralName, properties, foreignProperties):
        ABMFormFile.__init__(self, className, pluralName, 'backend_edit_form', properties)
        self.path = config['backend']['forms'] + className + 'Edit.php'
        self.addForeignVariablesToken(foreignProperties);
        self.addConstructorToken(foreignProperties);
        self.addMethodsTokens(foreignProperties);

    def addForeignVariablesToken(self, abms):
        subforms = ""
        counts   = ""
        for abm in abms:
            subforms += "    /**\n"
            subforms += "     * @var Zend_Form_SubForm\n"
            subforms += "     */\n"
            subforms += "    public $" + firstToLowercase(abm.plural_name) + ";\n"

            counts += self.declareCountVariable(abm)

        self.templateTokens['form_foreign_variables'] = subforms + "\n" + counts

    def addConstructorToken(self, abms):
        constructorParams    = ""
        variablesDeclaration = ""
        for abm in abms:
            constructorParams += self.constructorParams(abm)
            variablesDeclaration += self.variablesDeclaration(abm)
        constructorParams = constructorParams[:-1]
        constructorParams = constructorParams[:-1]

        constructor = "function __construct(" + constructorParams + ") {\n" + variablesDeclaration
        constructor += "        parent::__construct();\n"
        constructor += "    }\n"

        self.templateTokens['form_constructor'] = constructor

    def addMethodsTokens(self, abms):
        methods = ""
        methodsDeclaration = ""
        for abm in abms:
            methods += "        $this->_init" + abm.plural_name  + "();\n"

            methodsDeclaration += "    protected function _init" + abm.plural_name + "() {\n"
            methodsDeclaration += "        $this->" + firstToLowercase(abm.plural_name) + " = new Zend_Form_SubForm();\n"
            methodsDeclaration += "        $this->" + firstToLowercase(abm.plural_name) + "->setIsArray(true);\n\n"

            methodsDeclaration += self.foreignPropertiesDeclaration(abm, '    ', 0)

            methodsDeclaration += "            $this->" + firstToLowercase(abm.plural_name) + "->addSubForm($subform0, $i);\n"
            methodsDeclaration += "        }\n"
            methodsDeclaration += "        $this->addSubForm($this->" + firstToLowercase(abm.plural_name) + ", '" + firstToLowercase(abm.plural_name) + "');\n"
            methodsDeclaration += "    }\n\n"

        self.templateTokens['form_foreign_methods'] = methods
        self.templateTokens['form_foreign_methods_declaration'] = methodsDeclaration


    def foreignPropertiesDeclarationList(self, tab, deep, abms):
        if not abms:
            return ""
        else:
            methodsDeclaration =  (tab*deep) + "            $subform" + str(deep-1) + "->addSubForm($subform" + str(deep) + ", $i);\n"
            methodsDeclaration += (tab*deep) + "        }\n"
            return self.foreignPropertiesDeclaration(abms[0], tab, deep) + methodsDeclaration + self.foreignPropertiesDeclarationList(tab, deep, abms[1:])

    def foreignPropertiesDeclaration(self, abm, tab, deep):
        methodsDeclaration = ""
        propertiesDeclaration = ""
        for prop in abm.properties.keys():
            propertiesDeclaration += (tab*deep) + "            $" + prop + " = new Zend_Form_Element_Text('" + prop + "');\n"
            propertiesDeclaration += (tab*deep) + "            $" + prop + "->setLabel('" + prop + "');\n"
            propertiesDeclaration += (tab*deep) + "            $subform" + str(deep) + "->addElement($" + prop + ");\n\n"

        methodsDeclaration += (tab*deep) + "        for ($i = 0; $i < $this->_numberOf" + abm.plural_name + "; $i++) {\n"
        methodsDeclaration += (tab*deep) + "            $subform" + str(deep) + " = new Zend_Form_SubForm();\n"
        methodsDeclaration += (tab*deep) + "            $subform" + str(deep) + "->setIsArray(true);\n\n"
        methodsDeclaration += propertiesDeclaration

        return methodsDeclaration + self.foreignPropertiesDeclarationList(tab, deep+1, abm.foreignProperties)

    def declareCountVariable(self, abm):
        counts =  "    /**\n"
        counts += "     * @var int\n"
        counts += "     */\n"
        counts += "    protected $_numberOf" + abm.plural_name + ";\n"
        return counts + foldS(self.declareCountVariable, abm.foreignProperties)
    
    def constructorParams(self, abm):
        return "$numberOf" + abm.plural_name + ", " + foldS(self.constructorParams, abm.foreignProperties)

    def variablesDeclaration(self, abm):
        return "        $this->_numberOf" + abm.plural_name + " = $numberOf" + abm.plural_name + ";\n" + foldS(self.variablesDeclaration, abm.foreignProperties)



# =============================
# Backend Dbtable
# ============================================================================================================

class DBTableFile(ABMFile):
    def __init__(self, className, pluralName, properties = {}, tableName = None):
        ABMFile.__init__(self, className, pluralName, 'backend_dbtable')
        self.path = config['backend']['dbtables'] + className + '.php'
        self.tableName = tableName if tableName else self.templateTokens['lower_plural_name']
        self.templateTokens['table_name'] = self.tableName
        self.addTableToken(properties)

    def addTableToken(self, properties):
        tableToken = "/**\n"
        tableToken += ("create table " + self.tableName + " (\n")
        for key in properties.keys():
            tableToken += ("  " + key + " " + properties[key] + ",\n")
        tableToken += ("  primary key (id)\n")
        tableToken += (");\n*/")

        self.templateTokens['table'] = tableToken

# =============================
# Frontend Service
# ============================================================================================================

class ServiceFile(ABMFile):
    def __init__(self, className, pluralName):
        ABMFile.__init__(self, className, pluralName, None)
        self.path = config['frontend']['ng-services'] + firstToLowercase(pluralName) + '.js'
        print self.path

    def generateCode(self):
        MinCLASSNAME  = firstToLowercase(self.class_name)
        MinPLURALNAME = firstToLowercase(self.plural_name)
        self.addLine("var speakersFrontApp = angular.module('speakersFrontApp');")
        self.addLine("")
        self.addLine("(function() {")
        self.addLine("")
        self.addLine("  'use strict';")
        self.addLine("")
        self.addLine("  /**")
        self.addLine("   * @ngdoc function")
        self.addLine("   * @name speakersFrontApp.factory:" + MinPLURALNAME + "Service")
        self.addLine("   * @description")
        self.addLine("   * # " + MinPLURALNAME + "Service")
        self.addLine("   * Factory of the speakersFrontApp")
        self.addLine("   */")
        self.addLine("  speakersFrontApp.factory('" + MinPLURALNAME + "Service', function(dbConnectedService, api2URL) {")
        self.addLine("      var instance = {")
        self.addLine("          serviceName: '" + toRes(self.plural_name) + "',")
        self.addLine("          uriToPut: function(" + MinCLASSNAME + ") {")
        self.addLine("              return this.serviceName + '/' + " + MinCLASSNAME + ".id;")
        self.addLine("          },")
        self.addLine("          url: api2URL")
        self.addLine("      };")
        self.addLine("      return angular.extend(angular.copy(dbConnectedService), instance);")
        self.addLine("  });")
        self.addLine("})();")


# =============================
# Frontend Edit Controller
# ============================================================================================================

class EditControllerFile(ABMFile):
    def __init__(self, className, pluralName):
        ABMFile.__init__(self, className, pluralName, None)
        self.path = config['frontend']['ng-controllers'] + firstToLowercase(pluralName) + 'Edit.js'
        print self.path

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
        code = code.replace('MinCLASSNAME' , firstToLowercase(self.class_name))
        code = code.replace('MayPLURALNAME' , self.plural_name)
        code = code.replace('MinPLURALNAME' , firstToLowercase(self.plural_name))
        code = code.replace('SnakeCLASSNAME' , toSnakeCase(self.class_name))
        code = code.replace('MinTotalPLURALNAME' , self.plural_name.lower())
        code = code.replace('UrlPLURALNAME' , toRes(self.plural_name))
        self.code = code


# =============================
# Frontend List Controller
# ============================================================================================================

class ListControllerFile(ABMFile):
    def __init__(self, className, pluralName):
        ABMFile.__init__(self, className, pluralName, None)
        self.path = config['frontend']['ng-controllers'] + firstToLowercase(pluralName) + 'List.js'
        print self.path

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
        code = code.replace('MinPLURALNAME', firstToLowercase(self.plural_name))
        code = code.replace('UrlPLURALNAME', toRes(self.plural_name))
        code = code.replace('SnakePLURALNAME', toSnakeCase(self.plural_name))
        self.code = code


# =============================
# Frontend List View
# ============================================================================================================

class ListHtmlFile(ABMFile):
    def __init__(self, className, pluralName, table):
        ABMFile.__init__(self, className, pluralName, table)
        self.path = config['frontend']['ng-views'] + toRes(pluralName) + '-list.html'
        print self.path

    def generateCode(self):
        self.addLine('<div class="row">')
        self.addLine('  <div class="col-xs-9">')
        self.addLine('    <h1 style="margin-top:10px">' + self.class_name.upper() + '</h1>')
        self.addLine('  </div>')
        self.addLine('  <div class="col-xs-3">')
        self.addLine('      <div class="well">')
        self.addLine('          <button type="button" class="btn btn-default" ng-click="newItem()">')
        self.addLine('              <span class="glyphicon glyphicon-plus"></span> New ' + self.class_name)
        self.addLine('          </button>')
        self.addLine('      </div>')
        self.addLine('  </div>')
        self.addLine('</div> ')
        self.addLine('')
        self.generateTable()

    def generateTable(self):
        MinCLASSNAME  = firstToLowercase(self.class_name)
        UrlPLURALNAME = toRes(self.plural_name)
        self.addLine('<table ng-table="table" class="table table-hover">')
        self.addLine('  <tr ng-repeat="' + MinCLASSNAME + ' in $data">')
        for key in self.table.keys():
            self.addLine('      <td data-title="' + "'" + firstToUppercase(key) + "'" + '" sortable="'+ "'" + key + "'" + '">')
            self.addLine('          <div ng-bind="' + MinCLASSNAME + '.' + key + '"/>')
            self.addLine('      </td>')
        self.addLine('      <td style="width: 25%;">')
        self.addLine('          <a class="btn" href="#/' + UrlPLURALNAME + '/edit/{{' + MinCLASSNAME + '.id}}"><span class="glyphicon glyphicon-pencil"/></a>')
        self.addLine('          <a class="btn"ng-click="deleteItem(' + MinCLASSNAME + '.id)">   <span class="glyphicon glyphicon-trash"/></a>')
        self.addLine('      </td>')
        self.addLine('  </tr>')
        self.addLine('</table>')


# =============================
# Frontend Edit View
# ============================================================================================================

class EditHtmlFile(ABMFile):
    def __init__(self, className, pluralName, table):
        ABMFile.__init__(self, className, pluralName, table)
        self.path = config['frontend']['ng-views'] + toRes(pluralName) + '-edit.html'
        print self.path

    def generateCode(self):
        code = """<div class="row ng-scope">
  <div class="col-xs-9">
    <h1 style="margin-top:10px">MayCLASSNAME</h1>
  </div>
        <div class="col-xs-3">
      <div class="well">
        <div class="btn-group" uib-dropdown>
          <button id="split-button" type="button" class="btn btn-default"
            ng-init="relatedRecordSelected = relatedRecordSelected || relatedRecords[0]"
            ng-bind="relatedRecordSelected.buttonTitle" ng-click="relatedRecordSelected.add()"></button>
          <button type="button" class="btn btn-default" uib-dropdown-toggle>
            <span class="caret"></span>
            <span class="sr-only">Split button!</span>
          </button>
          <ul uib-dropdown-menu role="menu" aria-labelledby="split-button">
            <li role="menuitem" ng-repeat="relatedRecord in relatedRecords">
              <a href="" ng-click="relatedRecord.add()" ng-bind="relatedRecord.buttonTitle"></a>
            </li>
          </ul>
        </div>
      </div>
  </div>
</div>
"""
        
        self.code = code.replace('MayCLASSNAME', self.class_name.upper())

        self.addLine('<form name="form" class="form form-horizontal" novalidate ng-submit="save' + self.class_name + '(form)">')
        self.addLine('<div class="row">')
        self.addLine('  <div class="col-md-4">')
        self.addLine('      <h4>General</h4>')
        self.generateFields()
        self.addLine('  </div>')
        self.addLine('')
        self.addLine('  <div class="col-md-8">')
        self.addLine('    <!-- PARAMETRIC FIELDS -->')
        self.addLine('  </div>')
        self.addLine('')
        self.addLine('</div>')
        self.addLine('<div class="row">')
        self.addLine('  <div class="col-md-6">')
        self.addLine('      <div class="form-group">')
        self.addLine('          <div class="col-md-offset-3 col-md-9">')
        self.addLine('              <button type="submit" class="btn btn-primary"> Save ' + self.class_name + ' </button>')
        self.addLine('              <button type="button" class="btn btn-default" ng-click="backToList()"> Back to List </button>')
        self.addLine('          </div>')
        self.addLine('      </div>')
        self.addLine('  </div>')
        self.addLine('</div>')
        self.addLine('</form>')

    def generateFields(self):
        MinCLASSNAME  = firstToLowercase(self.class_name)
        for key in self.table.keys():
            if key != 'id':
                fiel_type  = self.table[key]
                input_text = '              <input type="text" name="' + key + '" class="form-control" ng-model="data.' + MinCLASSNAME + '.' + key + '" placeholder="' + firstToUppercase(key) + '"'
                
                if contains('varchar', fiel_type):
                    input_text += ' required maxlength="' + getNumber(fiel_type) + '" />'
                else:
                    input_text += ' required/>'

                self.addLine('      <div class="form-group">')
                self.addLine('          <label class="label-control col-md-3" for="' + key + '"> ' + firstToUppercase(key) + ' </label>')
                self.addLine('          <div class="col-md-9">')
                self.addLine(input_text)
                self.addLine('              <span class="error-message" ng-show="form.$submitted && form.' + key + '.$error.required">This field is required</span>')
                self.addLine('          </div>')
                self.addLine('      </div>')


# =============================
# Factories
# ============================================================================================================

class ABMCreator(object):
    def __init__(self, className, pluralName, properties = {}, foreignProperties = [], expansions = {}, tableName = None):
        self.class_name  = className
        self.plural_name = pluralName
        self.files = []
        self.properties = properties
        self.foreignProperties = foreignProperties
        self.expansions = expansions
        self.tableName = tableName

    # ======================================================
    # === Backend files
    # ======================================================
    def modelFile(self):
        self.files.append(ModelFile(self.class_name, self.plural_name, self.foreignProperties, self.expansions))
        return self

    def dbTableFile(self):
        self.files.append(DBTableFile(self.class_name, self.plural_name, self.properties, self.tableName))
        return self

    def formListFile(self):
        self.files.append(FormListFile(self.class_name, self.plural_name, self.properties))
        return self

    def formEditFile(self):
        self.files.append(FormEditFile(self.class_name, self.plural_name, self.properties, self.foreignProperties))
        return self

    def controllerFile(self):
        self.files.append(ControllerFile(self.class_name, self.plural_name, self.foreignProperties))
        return self

    def dtoFile(self):
        self.files.append(DtoFile(self.class_name, self.plural_name, self.properties, self.foreignProperties, self.expansions))
        return self

    def backendABM(self):
        return self.modelFile().dbTableFile().dtoFile().formListFile().formEditFile().controllerFile()

    # ======================================================
    # === Frontend files
    # ======================================================

    def serviceFile(self):
        self.files.append(ServiceFile(self.class_name, self.plural_name))
        return self

    def editControllerFile(self):
        self.files.append(EditControllerFile(self.class_name, self.plural_name))
        return self

    def listControllerFile(self):
        self.files.append(ListControllerFile(self.class_name, self.plural_name))
        return self

    def listHtmlFile(self):
        self.files.append(ListHtmlFile(self.class_name, self.plural_name, self.properties))
        return self

    def editHtmlFile(self):
        self.files.append(EditHtmlFile(self.class_name, self.plural_name, self.properties))
        return self

    def frontendABMFile(self):
        return self.serviceFile().editControllerFile().listControllerFile().listHtmlFile().editHtmlFile()

    # ======================================================
    # === Full ABMS
    # ======================================================
    def fullABM(self):
        return self.backendABM().frontendABMFile().appJsIndexInfo()

    def appJsIndexInfo(self):
        MayPLURALNAME = self.plural_name
        MinPLURALNAME = firstToLowercase(self.plural_name)
        ResPLURALNAME = toRes(self.plural_name)
        UrlPLURALNAME = toRes(self.plural_name)

        print("")
        print(".when('/" + UrlPLURALNAME + "',{")
        print("  templateUrl: 'views/" + ResPLURALNAME + "-list.html',")
        print("  controller : '" + MayPLURALNAME + "ListCtrl',")
        print("  resolve: speakersFrontApp.resolve" + MayPLURALNAME + "ListCtrl,")
        print("}).when('/" + UrlPLURALNAME + "/edit/:id',{")
        print("  templateUrl: 'views/" + ResPLURALNAME + "-edit.html',")
        print("  controller : '" + MayPLURALNAME + "EditCtrl',")
        print("  resolve: speakersFrontApp.resolve" + MayPLURALNAME + "EditCtrl")
        print("}).when('/" + UrlPLURALNAME + "/new',{")
        print("  templateUrl: 'views/" + ResPLURALNAME + "-edit.html',")
        print("  controller : '" + MayPLURALNAME + "EditCtrl',")
        print("  resolve: speakersFrontApp.resolve" + MayPLURALNAME + "EditCtrl")
        print("})")
        print("")
        print('<li ng-class="getNavSidebarClassItem(' + "'/" + UrlPLURALNAME + "')" + '"' + '><a ng-href="#/' + UrlPLURALNAME + '">' + self.plural_name + '</a></li>')
        print("")
        print('<script src="scripts/services/' + MinPLURALNAME + '.js"></script>')
        print("")
        print('<script src="scripts/controllers/' + MinPLURALNAME + 'List.js"></script>')
        print("")
        print('<script src="scripts/controllers/' + MinPLURALNAME + 'Edit.js"></script>')
        print('')
        return self

    def onTheFlyChanges(self, entityName, entityPluralName):
        code = """------------------------------------------------------------------
in: app/views/UrlPLURALNAME-edit.html
<a href="" ng-click="newEntityMayCLASSNAME()">New EntityMayCLASSNAME</a>

------------------------------------------------------------------
in: app/scripts/controllers/MinPLURALNAMEEdit.js
$scope.newEntityMayCLASSNAME = function() {
    var modalInstance = $uibModal.open({
        templateUrl: 'views/EntityMinPLURALNAME-edit.html',
        controller: 'EntityMayPLURALNAMEEditCtrl',
        size: 'lg',
        resolve: angular.extend(angular.copy(speakersFrontApp.absResolveEntityMayPLURALNAMEEditCtrl), {
            data: function($route, EntityMinPLURALNAMEService) {
                return { EntityMinCLASSNAME: {} }; //Needs the empty case of app/scripts/controllers/EntityMayCLASSNAMEEdit.js
            }
        })
    });

    modalInstance.result.then(function(response) {
        console.log(response);
        $scope.EntityMinPLURALNAME.push(response.EntityMinCLASSNAME);
        $scope.data.MinCLASSNAME.EntityMinCLASSNAMEId = response.EntityMinCLASSNAME.id;
    });
}

------------------------------------------------------------------
in: app/scripts/controllers/EntityMayCLASSNAMEEdit.js

add $uibModalInstance to the parameters of controller.

$scope.backToList = function(){
    if ($uibModalInstance) {
        $uibModalInstance.dismiss();
    } else {
        window.location = '#/EntityMinPLURALNAME';
    }
};

$scope.saveEntityMayCLASSNAME = function(form){
    if (form.$valid) {
        EntityMinPLURALNAMEService.save($scope.data.EntityMinCLASSNAME, $scope.data.isNew).then(function(response){
            if ($uibModalInstance) {
                $uibModalInstance.close(response);
            } else {
                window.location = '#/EntityMinPLURALNAME';
            }
        });
    }
};

speakersFrontApp.resolveEntityMayPLURALNAMEEditCtrl = angular.extend(angular.copy(speakersFrontApp.absResolveEntityMayPLURALNAMEEditCtrl), {
  $uibModalInstance: function(){
    return null;
  },
});
"""
        code = code.replace('EntityMayCLASSNAME', entityName)
        code = code.replace('EntityMinCLASSNAME', firstToLowercase(entityName))
        code = code.replace('EntityMayPLURALNAME', entityPluralName)
        code = code.replace('EntityMinPLURALNAME', firstToLowercase(entityPluralName))
        code = code.replace('MayCLASSNAME', self.class_name)
        code = code.replace('MinCLASSNAME', firstToLowercase(self.class_name))
        code = code.replace('MayPLURALNAME', self.plural_name)
        code = code.replace('MinPLURALNAME', firstToLowercase(self.plural_name))
        code = code.replace('UrlPLURALNAME', toRes(self.plural_name))
        code = code.replace('SnakePLURALNAME', toSnakeCase(self.plural_name))
        print(code)

    def execute(self):
        for abmFile in self.files + self.foreignProperties:
            abmFile.execute()


# =============================
# MAIN
# ============================================================================================================

if __name__ == "__main__":
    eventProperties = {
        'id': 'integer not null auto_increment',
        'name': 'varchar(100)',
        'longDescription': 'text',
        'shortDescription': 'varchar(255)',
        'link': 'varchar(255)',
        'city': 'varchar(50)',
        'location': 'varchar(255)',
        'image': 'varchar(255)',
        'countryCode': 'varchar(3)',
        'creationDate': 'timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
        'startDate': 'timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
        'endDate': 'timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
    }

    eventSpeakerProp = {
        'id': 'integer not null auto_increment',
        'eventId': 'integer',
        'speakerId': 'integer',
        'shortDescription': 'varchar(255)'
    }

    eventSubeventProp = {
        'id': 'integer not null auto_increment',
        'eventId': 'integer',
        'name': 'varchar(100)',
        'longDescription': 'text',
        'shortDescription': 'varchar(255)',
        'startDate': 'timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
        'endDate': 'timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
    }

    eventForeignProperties = [
        ABMCreator('EventSpeaker',  'EventSpeakers',  eventSpeakerProp, tableName="eventsSpeakers" ).dbTableFile().dtoFile(),
        ABMCreator('EventSubevent', 'EventSubevents', eventSubeventProp, tableName="eventsSubevents").dbTableFile().dtoFile()
    ]

    eventExpansions = {
        'list': {
            'countryCode': {
                'dbtable': 'country',
                'pk': 'code'
            }
        },
        'single': {
            'eventSubevent': {
                'dbtable': 'eventSubevent',
                'pk':'id'
            },
            'eventSpeaker': {
                'dbtable': 'eventSpeaker',
                'pk':'id'
            }
        }
    }

    ABMCreator('Event', 'Events', eventProperties, eventForeignProperties, eventExpansions).backendABM().execute()
    
    countryProperties = {
        'code': 'varchar(3)',
        'name': 'varchar(100)',
    }
    ABMCreator('Country', 'Countries', countryProperties).dbTableFile().dtoFile().execute()