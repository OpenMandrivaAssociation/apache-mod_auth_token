#Module-Specific definitions
%define mod_name mod_auth_token
%define mod_conf A63_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Token based authentication to secure downloads and prevent deep-linking
Name:		apache-%{mod_name}
Version:	1.0.3
Release:	%mkrel 9
Group:		System/Servers
License:	GPL
URL:		http://www.synd.info/
Source0:	http://www.synd.info/downloads/releases/%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.8
Requires(pre):	apache >= 2.2.8
Requires:	apache-conf >= 2.2.8
Requires:	apache >= 2.2.8
BuildRequires:  apache-devel >= 2.2.8
BuildRequires:	file
BuildRequires:	autoconf2.5
BuildRequires:	automake
BuildRequires:	libtool
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This module uses token based authentication to secure downloads and prevent
deep-linking. Have your PHP script or servlet generate the to authenticate the
download. Apache can then treat the download request like a normal file
transfer without having to pipe the file through a script in  order to add
authentication.

%prep

%setup -q -n %{mod_name}-%{version}

cp %{SOURCE1} %{mod_conf}

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type d -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type d -name .svn` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
rm -f configure
libtoolize --copy --force; aclocal; autoconf; automake --add-missing --copy --foreign && autoconf

%configure2_5x --localstatedir=/var/lib \
    --with-apxs=%{_sbindir}/apxs

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog LICENSE README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
