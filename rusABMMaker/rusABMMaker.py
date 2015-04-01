first_to_lowercase = lambda s: s[:1].lower() + s[1:] if s else ''

class AbmCode():
	def __init__(self, className, variables):
		self.code = ""
		self.class_name = className
		self.variables = variables

	def param_name(self):
		return first_to_lowercase(self.class_name)

	def addLine(self, aLine):
		self.code += ("\n" + aLine)

	def generateInstanceVariables(self):
		for varName in self.variables.keys():
			self.addLine("	private " + variables.get(varName) + " " + varName + ";")

	def addSeparator(self):
		self.addLine("")
		self.addLine("-------------------------------------------------------------------------")
		self.addLine("")

	def generateClassCode(self):
		self.addLine("import javax.persistence.Entity;")
		self.addLine("import javax.persistence.Table;")
		self.addLine("")
		self.addLine("import coop.tecso.foundation.persistence.model.AbstractPersistentObject;")
		self.addLine("")
		self.addLine("@Entity")
		self.addLine("@Table(name=" + stringVariable("sin_" + self.param_name()) + ")")
		self.addLine("public class " + self.class_name + " extends AbstractPersistentObject{")
		self.addLine("")
		self.generateInstanceVariables()
		self.addLine("}")

	def generateDAOCode(self):
		self.addLine("import java.util.List;")
		self.addLine("")
		self.addLine("import coop.tecso.search.service.impl.PagedFinder")
		self.addLine("")
		self.addLine("public interface " + self.class_name + "DAO {")
		self.addLine("")
		self.addLine("	PagedFinder searchPaginado(PagedFinder pf);")
		self.addLine("")
		self.addLine("	List<" + self.class_name + "> findAll();")
		self.addLine("")
		self.addLine("	" + self.class_name + " findById(Long id);")
		self.addLine("")
		self.addLine("	void save(" + self.class_name + " " + self.param_name() + ");")
		self.addLine("")
		self.addLine("	void delete(" + self.class_name + " " + self.param_name() + ");")
		self.addLine("}")

	def generateDAOImplCode(self):
		self.addLine("import java.util.List;")
		self.addLine("")
		self.addLine("@Repository")
		self.addLine("public class " + self.class_name + "DAOImpl extends PersistentObjectDAOImpl<" + self.class_name + "> implements " + self.class_name + "DAO {")
		self.addLine("")
		self.addLine("")



def stringVariable(aVariable):
	return '"' + aVariable + '"'

className = 'ParametroSiniestro'
variables = {
		'clase':'ClaseParametroSiniestro',
		'descripcion':'String',
		'strValor':'String'
		}

abm = AbmCode(className, variables)
abm.generateClassCode()
abm.addSeparator()
abm.generateDAOCode()
abm.addSeparator()
abm.generateDAOImplCode()


print(abm.code)