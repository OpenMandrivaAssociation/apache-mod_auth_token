#Module-Specific definitions
%define mod_name mod_auth_token
%define mod_conf A63_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Token based authentication to secure downloads and prevent deep-linking
Name:		apache-%{mod_name}
Version:	1.0.3
Release:	11
Group:		System/Servers
License:	GPL
URL:		https://www.synd.info/
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
    --with-apxs=%{_bindir}/apxs

%make

%install

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

%files
%doc AUTHORS ChangeLog LICENSE README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-10mdv2012.0
+ Revision: 772589
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-9
+ Revision: 678271
- mass rebuild

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-8mdv2011.0
+ Revision: 627724
- don't force the usage of automake1.7

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-7mdv2011.0
+ Revision: 587929
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-6mdv2010.1
+ Revision: 516058
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-5mdv2010.0
+ Revision: 406546
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-4mdv2009.1
+ Revision: 325565
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-3mdv2009.0
+ Revision: 234688
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-2mdv2009.0
+ Revision: 215539
- fix rebuild
- hard code %%{_localstatedir}/lib to ease backports

* Tue May 06 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-1mdv2009.0
+ Revision: 201980
- 1.0.3

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-5mdv2008.1
+ Revision: 181673
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-4mdv2008.0
+ Revision: 82526
- rebuild


* Sun Mar 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-3mdv2007.1
+ Revision: 141274
- rebuild
- rebuild

* Mon Feb 12 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-1mdv2007.1
+ Revision: 118915
- 1.0.2
- bunzip sources

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-2mdv2007.1
+ Revision: 79339
- Import apache-mod_auth_token

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-2mdv2007.0
- rebuild

* Tue May 16 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-1mdk
- initial Mandriva package

