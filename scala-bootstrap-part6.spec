Name:		scala-bootstrap-part6
Version:	1
Release:	1
Summary:	Sixth checkpoint of the Scala 2.10.7 bootstrap climb
Group:		Development/Java
License:	Apache-2.0
URL:		https://github.com/vxtls/scala
Source0:	scala-bootstrap-2.10.7.tar.gz
Patch0:		scala-bootstrap-part6-stop.patch

BuildArch:	noarch
BuildRequires:	scala-bootstrap-part5 = 1
BuildRequires:	java-1.8.0-openjdk-devel
BuildRequires:	git-core
BuildRequires:	make
BuildRequires:	python
BuildRequires:	tar
BuildRequires:	patch

%description
Checkpoint of the vxtls Scala bootstrap climb from
v2.10.0-M2+5e4c47f through v2.10.0-M3+8ce4787.
It resumes from the scala-bootstrap-part5 seed.
This package does not provide the Scala 2.10.7 compiler.

%prep
%autosetup -n scala-bootstrap-2.10.7 -p1
find . -type f \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -print > binaries.list
if [ -s binaries.list ]; then
	cat binaries.list
	exit 1
fi
test -s LICENSE
test -s compile.sh
test -s scripts/pack-seed.sh
test -s scripts/check-part.sh
test -s scripts/buildit.sh
grep -q resume_skip scripts/buildit.sh
grep -q SCALA_BOOT_UNTIL compile.sh
grep -q SCALA_BOOT_SEED compile.sh
grep -q bcp-flag scripts/pack-seed.sh
grep -q bcp-flag scripts/check-part.sh
grep -q GROUP5 scripts/pack-seed.sh
test "$(grep -c group4_uses_source_fjbg scripts/pack-seed.sh)" = 2

%build
set -eo pipefail
export JAVA_HOME=$(ls -d %{_jvmdir}/java-1.8.0-openjdk-* | head -n 1)
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
export SCALA_BOOT_SEED=%{_datadir}/scala-bootstrap-part5/seed
export SCALA_BOOT_FROM=v2.10.0-M2+5e4c47f-bootstrap
export SCALA_BOOT_UNTIL=v2.10.0-M3+8ce4787-bootstrap
bash ./compile.sh

%install
set -eo pipefail
mkdir -p %{buildroot}%{_datadir}/scala-bootstrap-part6
cp -a dist/seed %{buildroot}%{_datadir}/scala-bootstrap-part6/
test -s %{buildroot}%{_datadir}/scala-bootstrap-part6/seed/until-stage
grep -qx 'v2.10.0-M3+8ce4787-bootstrap' %{buildroot}%{_datadir}/scala-bootstrap-part6/seed/until-stage
grep -qx 'v2.10.0-M3+6bb5975-bootstrap' %{buildroot}%{_datadir}/scala-bootstrap-part6/seed/next-stage
grep -qx 'v2.10.0-M3+8ce4787-bootstrap' %{buildroot}%{_datadir}/scala-bootstrap-part6/seed/pred-stage
grep -qx -- '-javabootclasspath' %{buildroot}%{_datadir}/scala-bootstrap-part6/seed/bcp-flag
grep -qx 1 %{buildroot}%{_datadir}/scala-bootstrap-part6/seed/scala-boot-lib
test -s %{buildroot}%{_datadir}/scala-bootstrap-part6/seed/stages/v2.10.0-M3+8ce4787-bootstrap/build/pack/lib/scala-compiler.jar
test -s %{buildroot}%{_datadir}/scala-bootstrap-part6/seed/stages/v2.10.0-M3+8ce4787-bootstrap/build/java8-charbuffer-overrides.jar
test -s %{buildroot}%{_datadir}/scala-bootstrap-part6/seed/stages/v2.10.0-M3+8ce4787-bootstrap/build/java8-legacy-stubs.jar
test -s %{buildroot}%{_datadir}/scala-bootstrap-part6/seed/stages/v2.10.0-M3+8ce4787-bootstrap/build/java8-filtered-stubs.jar
test -s %{buildroot}%{_datadir}/scala-bootstrap-part6/seed/stages/v2.10.0-M3+8ce4787-bootstrap/build/libs/forkjoin.jar
if [ -e %{buildroot}%{_datadir}/scala-bootstrap-part6/seed/stages/way2scala-2.0-stage10-bootstrap/distribs/unix/scala-2.0-stage10-bootstrap/share/scala/lib/fjbg.jar ]; then
	echo fjbg jar is not a seed of this checkpoint
	exit 1
fi

%check
set -eo pipefail
export JAVA_HOME=$(ls -d %{_jvmdir}/java-1.8.0-openjdk-* | head -n 1)
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
bash ./scripts/check-part.sh %{buildroot}%{_datadir}/scala-bootstrap-part6/seed

%files
%{_datadir}/scala-bootstrap-part6
%license LICENSE
