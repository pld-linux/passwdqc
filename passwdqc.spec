Summary:	A password/passphrase strength checking and policy enforcement toolset
Name:		passwdqc
Version:	1.3.0
Release:	1
License:	BSD
Group:		Base
URL:		http://www.openwall.com/passwdqc/
Source0:	http://www.openwall.com/passwdqc/%{name}-%{version}.tar.gz
# Source0-md5:	3225280caba817c7009dffc157efc1b9
BuildRequires:	pam-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
passwdqc is a password/passphrase strength checking and policy
enforcement toolset, including a PAM module (pam_passwdqc),
command-line programs (pwqcheck and pwqgen), and a library
(libpasswdqc).

pam_passwdqc is normally invoked on password changes by programs such
as passwd(1). It is capable of checking password or passphrase
strength, enforcing a policy, and offering randomly-generated
passphrases, with all of these features being optional and easily
(re-)configurable.

pwqcheck and pwqgen are standalone password/passphrase strength
checking and random passphrase generator programs, respectively, which
are usable from scripts.

libpasswdqc is the underlying library, which may also be used from
third-party programs.

%package devel
Summary:	Libraries and header files for building passwdqc-aware applications
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains development libraries and header files needed
for building passwdqc-aware applications.

%package -n pam-pam_passwdqc
Summary:	Password quality-control PAM module
Group:		Base
Requires:	%{name} = %{version}-%{release}

%description -n pam-pam_passwdqc
The pam_passwdqc module is a simple password strength checking module
for PAM. In addition to checking regular passwords, it offers support
for passphrases and can provide randomly generated ones.

%prep
%setup -q

%build
sed -i -e 's#^CC =.*#CC = %{__cc}#g' Makefile

%{__make}
	CC="%{_cc}" \
	CFLAGS_lib="-Wall -W -fPIC -DLINUX_PAM %{rpmcflags}_lib %{rpmcppflags}" \
	CFLAGS_bin="-Wall -W %{rpmcflags} %{rpmcppflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir} \
	SHARED_LIBDIR=/%{_lib} \
	DEVEL_LIBDIR=%{_libdir} \
	SECUREDIR=/%{_lib}/security

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README pwqcheck.php
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/passwdqc.conf
%attr(755,root,root) /%{_lib}/libpasswdqc.so.0
%attr(755,root,root) %{_bindir}/pwqcheck
%attr(755,root,root) %{_bindir}/pwqgen
%{_mandir}/man1/pwqcheck.1*
%{_mandir}/man1/pwqgen.1*
%{_mandir}/man5/passwdqc.conf.5*

%files devel
%defattr(644,root,root,755)
%{_includedir}/passwdqc.h
%attr(755,root,root) %{_libdir}/libpasswdqc.so

%files -n pam-pam_passwdqc
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/security/pam_passwdqc.so
%{_mandir}/man8/pam_passwdqc.8*
