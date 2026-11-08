Name:		doxia-skin-model
Version:	2.1.0
Release:	1
Summary:	Doxia skin model
Group:		Development/Java
License:	ASL 2.0
URL:		https://maven.apache.org/doxia/doxia-sitetools/
Source0:	https://repo1.maven.org/maven2/org/apache/maven/doxia/doxia-skin-model/%{version}/doxia-skin-model-%{version}-sources.jar
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:	plexus-utils >= 3.6.2
Requires:	plexus-utils >= 3.6.2
BuildRequires:	mvn(org.codehaus.plexus:plexus:pom::)
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

%description
The Doxia skin model. A skin can include a resource only when a
condition matches. The tag ships the Modello descriptor. The generated
model classes come from the upstream sources jar. XML classes come
from plexus-utils.

%prep
%setup -q -c -T
# The builders' rpmuncompress passes a sources jar to tar.
python - %{SOURCE0} <<'PY'
import sys
import zipfile
zipfile.ZipFile(sys.argv[1]).extractall(".")
PY
python - <<'PY'
import os
import shutil
import xml.etree.ElementTree as ET

for name in ("LICENSE", "NOTICE"):
    src = os.path.join("META-INF", name)
    if os.path.exists(src):
        shutil.copy2(src, name)
os.makedirs("src/main/java", exist_ok=True)
shutil.move("org", "src/main/java/org")

NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)

def tag(name):
    return "{" + NS + "}" + name

def add(parent, name, text):
    node = ET.SubElement(parent, tag(name))
    node.text = text
    return node

root = ET.Element(tag("project"))
add(root, "modelVersion", "4.0.0")
add(root, "groupId", "org.apache.maven.doxia")
add(root, "artifactId", "doxia-skin-model")
add(root, "version", "%{version}")
add(root, "name", "Doxia Sitetools :: Skin model")
props = ET.SubElement(root, tag("properties"))
add(props, "maven.compiler.release", "8")
add(props, "project.build.sourceEncoding", "UTF-8")
deps = ET.SubElement(root, tag("dependencies"))
dep = ET.SubElement(deps, tag("dependency"))
add(dep, "groupId", "org.codehaus.plexus")
add(dep, "artifactId", "plexus-utils")
add(dep, "version", "3.6.2")
ET.ElementTree(root).write("pom.xml", encoding="utf-8", xml_declaration=True)
PY

%files -f .mfiles
%doc LICENSE NOTICE
