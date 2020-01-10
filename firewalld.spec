%if (0%{?fedora} >= 13 || 0%{?rhel} > 7)
%global with_python3 1
%if (0%{?fedora} >= 23 || 0%{?rhel} >= 8)
%global use_python3 1
%endif
%endif

Summary: A firewall daemon with D-Bus interface providing a dynamic firewall
Name: firewalld
Version: 0.5.3
Release: 5%{?dist}
URL:     http://www.firewalld.org
License: GPLv2+
Source0: https://github.com/firewalld/firewalld/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch1: firewalld-0.4.4.3-qt4_applet.patch
Patch2: firewalld-0.4.4.3-exclude_firewallctl_rhbz#1374799.patch
Patch3: 0001-ipset-check-type-when-parsing-ipset-definition.patch
Patch4: 0002-firewall-core-io-functions-add-check_config.patch
Patch5: 0003-firewall-offline-cmd-add-check-config-option.patch
Patch6: 0004-firewall-cmd-add-check-config-option.patch
Patch7: 0005-tests-firewall-cmd-exercise-check-config.patch
Patch8: 0001-firewall.core.fw_nm-avoid-iterating-NM-devices-conne.patch
Patch9: 0002-firewall.core.fw_nm-identify-the-connections-by-uuid.patch
Patch10: 0003-firewall.core.fw_nm-ignore-generated-connections.patch
Patch11: 0001-tests-functions-check-state-after-a-reload.patch
Patch12: 0002-fw-on-restart-set-policy-from-same-function.patch
Patch13: 0003-fw-if-failure-occurs-during-startup-set-state-to-FAI.patch
Patch14: 0001-fw-if-startup-fails-on-reload-reapply-non-perm-confi.patch
Patch15: 0002-fw-If-direct-rules-fail-to-apply-add-a-Direct-label-.patch

BuildArch: noarch
BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: intltool
# glib2-devel is needed for gsettings.m4
BuildRequires: glib2, glib2-devel
BuildRequires: systemd-units
BuildRequires: docbook-style-xsl
BuildRequires: libxslt
BuildRequires:  python2-devel
BuildRequires: iptables, ebtables, ipset
%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif #0%{?with_python3}
Requires: iptables, ebtables, ipset
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: firewalld-filesystem = %{version}-%{release}
%if 0%{?use_python3}
Requires: python3-firewall  = %{version}-%{release}
%else #0%{?use_python3}
Requires: python-firewall  = %{version}-%{release}
%endif #0%{?use_python3}
Conflicts: selinux-policy < 3.13.1-118.el7
Conflicts: squid < 7:3.5.10-1
Conflicts: NetworkManager < 1:1.4.0-3.el7

%description
firewalld is a firewall service daemon that provides a dynamic customizable 
firewall with a D-Bus interface.

%package -n python-firewall
Summary: Python2 bindings for firewalld
Provides: python2-firewall
Obsoletes: python2-firewall
Requires: dbus-python
Requires: python-slip-dbus
Requires: python-decorator
Requires: pygobject3-base
Conflicts: %{name} < 0.3.14

%description -n python-firewall
Python2 bindings for firewalld.

%if 0%{?with_python3}
%package -n python3-firewall
Summary: Python3 bindings for firewalld
Requires: python3-dbus
Requires: python3-slip-dbus
Requires: python3-decorator
%if (0%{?fedora} >= 23 || 0%{?rhel} >= 8)
Requires: python3-gobject-base
%else
Requires: python3-gobject
%endif
Conflicts: %{name} < 0.3.14

%description -n python3-firewall
Python3 bindings for firewalld.
%endif #0%{?with_python3}

%package -n firewalld-filesystem
Summary: Firewalld directory layout and rpm macros
Conflicts: %{name} < 0.3.13

%description -n firewalld-filesystem
This package provides directories and rpm macros which
are required by other packages that add firewalld configuration files.

%package -n firewall-applet
Summary: Firewall panel applet
Requires: %{name} = %{version}-%{release}
Requires: firewall-config = %{version}-%{release}
Requires: hicolor-icon-theme
%if 0%{?use_python3}
Requires: python3-PyQt4
Requires: python3-gobject
%else
Requires: PyQt4
Requires: pygobject3-base
%endif
Requires: libnotify
Requires: NetworkManager-libnm
Requires: dbus-x11

%description -n firewall-applet
The firewall panel applet provides a status information of firewalld and also 
the firewall settings.

%package -n firewall-config
Summary: Firewall configuration application
Requires: %{name} = %{version}-%{release}
Requires: hicolor-icon-theme
Requires: gtk3
%if 0%{?use_python3}
Requires: python3-gobject
%else
Requires: pygobject3-base
%endif
Requires: NetworkManager-libnm
Requires: dbus-x11

%description -n firewall-config
The firewall configuration application provides an configuration interface for 
firewalld.

%prep
%autosetup -p1
./autogen.sh

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%if 0%{?use_python3}
sed -i -e 's|/usr/bin/python -Es|%{__python3} -Es|' %{py3dir}/fix_python_shebang.sh
sed -i 's|/usr/bin/python|%{__python3}|' %{py3dir}/config/lockdown-whitelist.xml
%endif #0%{?use_python3}
%endif #0%{?with_python3}

%build
autoreconf --force -v --install --symlink
%configure --enable-sysconfig --enable-rpmmacros
make %{?_smp_mflags}

%if 0%{?with_python3}
pushd %{py3dir}
autoreconf --force -v --install --symlink
%configure --enable-sysconfig --enable-rpmmacros PYTHON=%{__python3}
make %{?_smp_mflags}
popd
%endif #0%{?with_python3}

%install
%if 0%{?use_python3}
make -C src install-nobase_dist_pythonDATA PYTHON=%{__python2} DESTDIR=%{buildroot}
%else
make install PYTHON=%{__python2} DESTDIR=%{buildroot}
%endif #0%{?use_python3}

%if 0%{?with_python3}
pushd %{py3dir}
%if 0%{?use_python3}
make install PYTHON=%{__python3} DESTDIR=%{buildroot}
%else
make -C src install-nobase_dist_pythonDATA PYTHON=%{__python3} DESTDIR=%{buildroot}
%endif #0%{?use_python3}
popd
%endif #0%{?with_python3}

desktop-file-install --delete-original \
  --dir %{buildroot}%{_sysconfdir}/xdg/autostart \
  %{buildroot}%{_sysconfdir}/xdg/autostart/firewall-applet.desktop
desktop-file-install --delete-original \
  --dir %{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/firewall-config.desktop

%find_lang %{name} --all-name

%post
%systemd_post firewalld.service

%preun
%systemd_preun firewalld.service

%postun
%systemd_postun_with_restart firewalld.service 


%post -n firewall-applet
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun -n firewall-applet
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans -n firewall-applet
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%post -n firewall-config
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun -n firewall-config
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans -n firewall-config
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f %{name}.lang
%doc COPYING README
%{_sbindir}/firewalld
%{_bindir}/firewall-cmd
%{_bindir}/firewall-offline-cmd
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/firewall-cmd
%{_prefix}/lib/firewalld/icmptypes/*.xml
%{_prefix}/lib/firewalld/ipsets/README
%{_prefix}/lib/firewalld/services/*.xml
%{_prefix}/lib/firewalld/zones/*.xml
%{_prefix}/lib/firewalld/helpers/*.xml
%{_prefix}/lib/firewalld/xmlschema/check.sh
%{_prefix}/lib/firewalld/xmlschema/*.xsd
%attr(0750,root,root) %dir %{_sysconfdir}/firewalld
%config(noreplace) %{_sysconfdir}/firewalld/firewalld.conf
%config(noreplace) %{_sysconfdir}/firewalld/lockdown-whitelist.xml
%attr(0750,root,root) %dir %{_sysconfdir}/firewalld/helpers
%attr(0750,root,root) %dir %{_sysconfdir}/firewalld/icmptypes
%attr(0750,root,root) %dir %{_sysconfdir}/firewalld/ipsets
%attr(0750,root,root) %dir %{_sysconfdir}/firewalld/services
%attr(0750,root,root) %dir %{_sysconfdir}/firewalld/zones
%dir %{_datadir}/firewalld
%defattr(0644,root,root)
%config(noreplace) %{_sysconfdir}/sysconfig/firewalld
#%attr(0755,root,root) %{_initrddir}/firewalld
%{_unitdir}/firewalld.service
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/FirewallD.conf
%{_datadir}/polkit-1/actions/org.fedoraproject.FirewallD1.desktop.policy.choice
%{_datadir}/polkit-1/actions/org.fedoraproject.FirewallD1.server.policy.choice
%{_datadir}/polkit-1/actions/org.fedoraproject.FirewallD1.policy
%{_mandir}/man1/firewall*cmd*.1*
%{_mandir}/man1/firewalld*.1*
%{_mandir}/man5/firewall*.5*
%{_sysconfdir}/modprobe.d/firewalld-sysctls.conf

%files -n python-firewall
%attr(0755,root,root) %dir %{python2_sitelib}/firewall
%attr(0755,root,root) %dir %{python2_sitelib}/firewall/config
%attr(0755,root,root) %dir %{python2_sitelib}/firewall/core
%attr(0755,root,root) %dir %{python2_sitelib}/firewall/core/io
%attr(0755,root,root) %dir %{python2_sitelib}/firewall/server
%{python2_sitelib}/firewall/*.py*
%{python2_sitelib}/firewall/config/*.py*
%{python2_sitelib}/firewall/core/*.py*
%{python2_sitelib}/firewall/core/io/*.py*
%{python2_sitelib}/firewall/server/*.py*

%if 0%{?with_python3}
%files -n python3-firewall
%attr(0755,root,root) %dir %{python3_sitelib}/firewall
%attr(0755,root,root) %dir %{python3_sitelib}/firewall/__pycache__
%attr(0755,root,root) %dir %{python3_sitelib}/firewall/config
%attr(0755,root,root) %dir %{python3_sitelib}/firewall/config/__pycache__
%attr(0755,root,root) %dir %{python3_sitelib}/firewall/core
%attr(0755,root,root) %dir %{python3_sitelib}/firewall/core/__pycache__
%attr(0755,root,root) %dir %{python3_sitelib}/firewall/core/io
%attr(0755,root,root) %dir %{python3_sitelib}/firewall/core/io/__pycache__
%attr(0755,root,root) %dir %{python3_sitelib}/firewall/server
%attr(0755,root,root) %dir %{python3_sitelib}/firewall/server/__pycache__
%{python3_sitelib}/firewall/__pycache__/*.py*
%{python3_sitelib}/firewall/*.py*
%{python3_sitelib}/firewall/config/*.py*
%{python3_sitelib}/firewall/config/__pycache__/*.py*
%{python3_sitelib}/firewall/core/*.py*
%{python3_sitelib}/firewall/core/__pycache__/*.py*
%{python3_sitelib}/firewall/core/io/*.py*
%{python3_sitelib}/firewall/core/io/__pycache__/*.py*
%{python3_sitelib}/firewall/server/*.py*
%{python3_sitelib}/firewall/server/__pycache__/*.py*
%endif #0%{?with_python3}

%files -n firewalld-filesystem
%dir %{_prefix}/lib/firewalld
%dir %{_prefix}/lib/firewalld/helpers
%dir %{_prefix}/lib/firewalld/icmptypes
%dir %{_prefix}/lib/firewalld/ipsets
%dir %{_prefix}/lib/firewalld/services
%dir %{_prefix}/lib/firewalld/zones
%dir %{_prefix}/lib/firewalld/xmlschema
%{_rpmconfigdir}/macros.d/macros.firewalld

%files -n firewall-applet
%{_bindir}/firewall-applet
%defattr(0644,root,root)
%{_sysconfdir}/xdg/autostart/firewall-applet.desktop
%dir %{_sysconfdir}/firewall
%{_sysconfdir}/firewall/applet.conf
%{_datadir}/icons/hicolor/*/apps/firewall-applet*.*
%{_mandir}/man1/firewall-applet*.1*

%files -n firewall-config
%{_bindir}/firewall-config
%defattr(0644,root,root)
%{_datadir}/firewalld/firewall-config.glade
%{_datadir}/firewalld/gtk3_chooserbutton.py*
%{_datadir}/firewalld/gtk3_niceexpander.py*
%{_datadir}/applications/firewall-config.desktop
%{_datadir}/appdata/firewall-config.appdata.xml
%{_datadir}/icons/hicolor/*/apps/firewall-config*.*
%{_datadir}/glib-2.0/schemas/org.fedoraproject.FirewallConfig.gschema.xml
%{_mandir}/man1/firewall-config*.1*

%changelog
* Fri Aug 17 2018 Eric Garver <egarver@redhat.com> - 0.5.3-5
- even if startup failed, reapply non-permanent interface to zone assignments

* Thu Aug 16 2018 Eric Garver <egarver@redhat.com> - 0.5.3-4
- backport patches to enter failed state if startup fails

* Thu Jul 19 2018 Eric Garver <egarver@redhat.com> - 0.5.3-3
- backport patches to avoid NM for generated connections

* Tue Jun 12 2018 Eric Garver <egarver@redhat.com> - 0.5.3-2
- backport patches for --check-config option

* Tue May 15 2018 Eric Garver <egarver@redhat.com> - 0.5.3-1
- rebase package to v0.5.3

* Tue Dec 12 2017 Eric Garver <egarver@redhat.com> - 0.4.4.4-14
- services/high-availability: Add port 9929 (RHBZ#1486143)

* Wed Dec 06 2017 Eric Garver <egarver@redhat.com> - 0.4.4.4-13
- firewalld: also reload dbus config interface for global options
  (RHBZ#1514043)

* Wed Dec 06 2017 Eric Garver <egarver@redhat.com> - 0.4.4.4-12
- Fix and improve firewalld-sysctls.conf (RHBZ#1516881)

* Mon Sep 18 2017 Phil Sutter - 0.4.4.4-11
- core: Log unsupported ICMP types as informational only (RHBZ#1479951)
- doc: firewall-cmd: Document --query-* options return codes (RHBZ#1372716)
- doc: firewall-cmd: Document quirk in --reload option (RHBZ#1452137)
- firewall-cmd: Use colors only if output is a TTY (RHBZ#1368544)
- firewall-offline-cmd: Don't require root for help output (RHBZ#1445214)

* Wed Sep 06 2017 Eric Garver <egarver@redhat.com> - 0.4.4.4-10
- Add missing ports to RH-Satellite-6 service (RHBZ#1422149)

* Fri Aug 18 2017 Eric Garver <egarver@redhat.com> - 0.4.4.4-9
- Reload nf_conntrack sysctls after the module is loaded (RHBZ#1462977)

* Sun Aug 13 2017 Eric Garver <egarver@redhat.com> - 0.4.4.4-8
- Add NFSv3 service (a127d697177b) (RHBZ#1462088)

* Thu Aug 10 2017 Eric Garver <egarver@redhat.com> - 0.4.4.4-7
- firewall.functions: New function get_nf_nat_helpers (RHBZ#1452681)
- firewall.core.fw: Get NAT helpers and store them internally. (RHBZ#1452681)
- firewall.core.fw_zone: Load NAT helpers with conntrack helpers (RHBZ#1452681)
- firewalld.dbus: Add missing properties nf_conntrach_helper_setting and
  nf_conntrack_helpers (RHBZ#1452681)
- D-Bus interfaces: Fix GetAll for interfaces without properties (RHBZ#1452017)
- firewall.server.firewalld: New property for NAT helpers supported by the
  kernel (RHBZ#1452681)

* Mon Jun 12 2017 Thomas Woerner <twoerner@redhat.com> - 0.4.4.4-6
- IPv6 ICMP type only rich-rule fix (cf50bd0) (RHBZ#1459921)

* Wed May 31 2017 Thomas Woerner <twoerner@redhat.com> - 0.4.4.4-5
- Translation update for japanese (RHBZ#1382652)

* Wed May 17 2017 Thomas Woerner <twoerner@redhat.com> - 0.4.4.4-4
- Add services for oVirt: ovirt-imageio, ovirt-vmconsole, ovirt-storageconsole,
  ctbc and nrpe (RHBZ#1449158)
- Fix policy issue with the choice policies by using the .policy.choice
  extension (RHBZ#1449754)

* Wed May  3 2017 Thomas Woerner <twoerner@redhat.com> - 0.4.4.4-3
- Fix --{set,get}-{short,description} for zones (RHBZ#1416325)
- Man pages: Add sctp and dccp for ports, ... (RHBZ#1429808)
- Add support for new wait option in restore commands (RHBZ#1446162)

* Wed Apr  5 2017 Thomas Woerner <twoerner@redhat.com> - 0.4.4.4-2
- Add support for sctp and dccp in ports, source-ports and forward-ports
  (RHBZ#1429808)
- Fix firewall-offline-cmd --remove-service-from-zone= option (RHBZ#1438127)

* Mon Mar 27 2017 Thomas Woerner <twoerner@redhat.com> - 0.4.4.4-1
- Rebase to firewalld-0.4.4.4
  http://www.firewalld.org/2017/03/firewalld-0-4-4-4-release
- Drop references to fedorahosted.org from spec file and Makefile.am, use
  archive from github
- Fix inconsistent ordering of rules in INPUT_ZONE_SOURCE (issue#166)
  (RHBZ#1421222)
- Fix ipset overloading from /etc/firewalld/ipsets (RHBZ#1423941)
- Fix permanent rich rules using icmp-type elements (RHBZ#1434763)
- firewall-config: Deactivate edit, remove, .. buttons if there are no items
- Check if ICMP types are supported by kernel before trying to use them
  (RHBZ#1401978)
- firewall-config: Show invalid ipset type in the ipset configuration dialog
  in a special label (RHBZ#1419058)

* Fri Feb 10 2017 Thomas Woerner <twoerner@redhat.com> - 0.4.4.3-2
- Drop ghost flag on policy file again

* Wed Feb  8 2017 Thomas Woerner <twoerner@redhat.com> - 0.4.4.3-1
- Rebase to firewalld-0.4.4.3 (RHBZ#1414584)
- Support disabled automatic helper assignment in firewalld (RHBZ#1006225)
- Fix masquerade rules to be created always the same (RHBZ#1374001)
- Properly handle quoted ifcfg file values (RHBZ#1395348)
- Fix extension of ifcfg backup files (RHBZ#1400478)
- Complete icmp types list (RHBZ#1401978)
- Fix LOG rule placement for LogDenied (RHBZ#1402932)
- Show error messages from NM and do not trace back (RHBZ#1405562)
- Support icmp-type usage in rich rules (RHBZ#1409544)
- New service file for freeipa-trust (RHBZ#1411650)
- Fix --{set,get}-{short,description} for ipset in commands (RHBZ#1416325)
- Speed up large ipset file loading and import (RHBZ#1416817)
- Improve support for ipsets in firewalld (RHBZ#1419058)
- ALREADY_ errors should result in warnings and zero exit code (RHBZ#1420457)

* Wed Feb  8 2017 Thomas Woerner <twoerner@redhat.com> - 0.4.3.2-10
- Fix LOG rule placement for LogDenied (RHBZ#1402932)

* Thu Jan  5 2017 Thomas Woerner <twoerner@redhat.com> - 0.4.3.2-9
- Fix ZONE being blanked in ifcfg on reboot (RHBZ#1381314)

* Mon Sep 12 2016 Thomas Woerner <twoerner@redhat.com> - 0.4.3.2-8
- Exclude firewallctl (RHBZ#1374799)

* Tue Sep  6 2016 Thomas Woerner <twoerner@redhat.com> - 0.4.3.2-7
- Tolerate ipv6_rpfilter fail (RHBZ#1285769)
- Fix set_rules to copy the rule before extracting the table (RHBZ#1373260)
- Translation update (RHBZ#1273296)
- Conflict with NetworkManager < 1:1.4.0-3.el7 (RHBZ#1366288)

* Tue Aug 30 2016 Thomas Woerner <twoerner@redhat.com> - 0.4.3.2-6
- Do not use exit code 254 for {ALREADY,NOT}_ENABLED sequences (RHBZ#1366654)
- Fail with NOT_AUTHORIZED if authorization fails (RHBZ#1368549)
- firewall-cmd: Fix get and set description for permanent zones (RHBZ#1368949)
- Fix loading of service helpers in active zones (RHBZ#1371116)

* Tue Aug 16 2016 Thomas Woerner <twoerner@redhat.com> - 0.4.3.2-5
- Print errors and warnings to stderr additional patch (RHBZ#1360894)
- Fixed trace back in firewallctl (RHBZ#1367155)
- Fix client crash if systembus can not be aquired (RHBZ#1367038)
- Make ALREADY_ENABLED a warning (RHBZ#1366654)
- Added conflict to old squid package providing the squid.service file
  (RHBZ#1366308)
- Fixed firewall-cmd help typo (RHBZ#1367171)

* Wed Aug 10 2016 Thomas Woerner <twoerner@redhat.com> - 0.4.3.2-4
- Fixed firewall-config gettext usage (RHBZ#1361612)
- Fixed ifcfg file reader and writer (RHBZ#1362171)
- Fixed loading ipset entries from file in commands (RHBZ#1365198)
- Added conflicts to old main package to sub packages (RHBZ#1361669)
- Do not show settings of zones etc. without authentication (RHBZ#1357098)
- Fixed CVE-2016-5410 (RHBZ#1359296)

* Thu Jul 28 2016 Thomas Woerner <twoerner@redhat.com> - 0.4.3.2-3
- Fix test suite for command change (RHBZ#1360871)
- Fix test suite with stderr usage (RHBZ#1360894)
- Rebuild for wrong docdir without version (RHBZ#1057327#c7)

* Wed Jul 27 2016 Thomas Woerner <twoerner@redhat.com> - 0.4.3.2-2
- Updated conflict for selinux-policy (RHBZ#1304723)
- Fixed exit codes in command line clients (RHBZ#1357050)
- Fixed traceback in firewall-cmd without args (RHBZ#1357063)
- Fixed source docs in man pages and help output (RHBZ#1357888)
- Fixed rebuild of changed man pages (RHBZ#1360362)
- Use stderr for errors and warnings in command line tools (RHBZ#1360894)
- Fixed lockdown not denying invalid commands (RHBZ#1360871)

* Tue Jul  5 2016 Thomas Woerner <twoerner@redhat.com> - 0.4.3.2-1
- Rebase to 0.4.3.2
- Fix regression with unavailable optional commands
- All missing backend messages should be warnings
- Individual calls for missing restore commands
- Only one authenticate call for add and remove options and also sequences
- RH-Satellite-6 service now upstream
- Conflict for selinux-policy needed to be updated to newer release
  (RHBZ#1304723)

* Tue Jun 28 2016 Thomas Woerner <twoerner@redhat.com> - 0.4.3.1-1
- Rebase to 0.4.3.1
- firewall.command: Fix python3 DBusException message not interable error
- src/Makefile.am: Fix path in firewall-[offline-]cmd_test.sh while installing
- firewallctl: Do not trace back on list command without further arguments
- firewallctl (man1): Added remaining sections zone, service, ..
- firewallctl: Added runtime-to-permanent, interface and source parser,
  IndividualCalls setting
- firewall.server.config: Allow to set IndividualCalls property in config
  interface
- Fix missing icmp rules for some zones
- runProg: Fix issue with running programs
- firewall-offline-cmd: Fix issues with missing system-config-firewall
- firewall.core.ipXtables: Split up source and dest addresses for transaction
- firewall.server.config: Log error in case of loading malformed files in
  watcher
- Install and package the firewallctl man page

* Wed Jun 22 2016 Thomas Woerner <twoerner@redhat.com> - 0.4.3-3
- Readding RH-Satellite-6 service

* Wed Jun 22 2016 Thomas Woerner <twoerner@redhat.com> - 0.4.3-2
- Fixed typo in Requires(post)

* Wed Jun 22 2016 Thomas Woerner <twoerner@redhat.com> - 0.4.3-1
- Rebase to 0.4.3
- Rebase to the new upstream and new release (RHBZ#1302802)
- New firewallctl command line utility (RHBZ#1147959)
- Adds radius TCP ports (RHBZ#1219717)
- XSD enhancements for conflicting tag specification (RHBZ#1296573)
- Adds port for corosync-qnetd to high-availability service (RHBZ#1347530)

* Tue May 31 2016 Thomas Woerner <twoerner@redhat.com> - 0.4.2-1
- Rebase to 0.4.2
- Allows unspecifying zone binding for interfaces in firewall-config
  (RHBZ#1066037)
- Adds improved management of zone binding for interfaces, connections and
  sources (RHBZ#1083626)
- Adds commands to showing details of zones, services, .. (RHBZ#1147500)
- Adds a default logging option (RHBZ#1147951)
- Adds quiet option for firewall-offline-cmd (RHBZ#1220467)
- Adds support for zone chain usage in direct rules (RHBZ#1136801,
  RHBZ#1336881)
- Adds source port support in zones, services and rich rules (RHBZ#1214770)
- Adds services imap and smtps (RHBZ#1220196)
- Fixes runtime to permanent migration(RHBZ#1237242)
- Fixes removal of destination addresses for services in permanent view in
  firewall-config (RHBZ#1278281)
- Fixes firewall-config usage over ssh (RHBZ#1281416)
- Fixes reload disconnects with existing connections (RHBZ#1287449)
- Fixes ICMP packet drops while reloading (RHBZ#1288177)
- Adds option to add a new zone, service, .. from existing file (RHBZ#1292926)
- Adds improved checks for file readers, fixes error reporting of strings
  containing illegal characters (RHBZ#1303026)
- Transforms direct.passthrough errors into warnings (RHBZ#1301573)
- Reduced getprotobyname and getservbyname calls for NIS use (RHBZ#1305434)
- Fixes (repeated) firewalld reload by sending SIGHUP signal (RHBZ#1313023)
- Adds After=dbus.service to service file to fix shutdown (RHBZ#1313845)
- Adds ICMP block inversion support (RHBZ#1325335)
- Fixes local traffic issue with masquerading in default zone (RHBZ#1326130)
- Adds destination rich rules without an element (RHBZ#1326462)
- Fixes reload after default zone change to newly introduced zone (RHBZ#1273888)
- Fixes start without ipv6_rpfilter module (RHBZ#1285769)
- Adds log of denied packets option (RHBZ#1322505)

* Tue Sep 15 2015 Thomas Woerner <twoerner@redhat.com> - 0.3.9-14
- Fixed file mode of schema configuration file verifier check.sh als in files
  (RHBZ#994479)

* Fri Sep 11 2015 Thomas Woerner <twoerner@redhat.com> - 0.3.9-13
- Fixed file mode of schema configuration file verifier check.sh (RHBZ#994479)
- Include upstream testsuite in SRPM package (RHBZ#1261502)
- Added missing ports to RH-Satellite-6 mservice (RHBZ#1254531)

* Mon Jul  6 2015 Thomas Woerner <twoerner@redhat.com> - 0.3.9-12
- New schema configuration file verifier (RHBZ#994479)
- More information about interface handling with and without NetworkManager
  (RHBZ#1122739) (RHBZ#1128563)
- Apply all rich rules for non-default targets (RHBZ#1142741)
- New iscsi service (RHBZ#1150656)
- New rsync service (RHBZ#1150659)
- ipXtables: use -w or -w2 if supported (RHBZ#1161745)
- Do not use ipv6header for protocol matching. (RHBZ#1164605)
- Iptables does not like limit of 1/d (RHBZ#1176813)
- Fix readdition of removed permanent direct settings (RHBZ#1182671)
- Fix bugs found by upstream test suite (RHBZ#1183008)
- Fix polkit auth for query and get passthroughs methods (RHBZ#1183688)
- New vdsm service (RHBZ#1194382)
- New freeipa services (RHBZ#1206490)
- Add missing parts to firewall-offline-cmd man page (RHBZ#1217678)

* Tue Jan 13 2015 Thomas Woerner <twoerner@redhat.com> - 0.3.9-11
- added missing upstream commit 265bfe90 for (RHBZ#993650)
- also add log message in the firewall-cmd output (RHBZ#1057095)

* Mon Oct 20 2014 Thomas Woerner <twoerner@redhat.com> - 0.3.9-10
- additional upstream commits for (RHBZ#993650)
- additional upstream commits for (RHBZ#1127706)

* Tue Oct  7 2014 Thomas Woerner <twoerner@redhat.com> - 0.3.9-9
- added lost runtime passthrough check and reverse patch (RHBZ#993650)

* Mon Sep 29 2014 Thomas Woerner <twoerner@redhat.com> - 0.3.9-8
- fixed GUI missing name of active zone (RHBZ#993655)
- recreate man pages at build time (RHBZ#1071303)
  - fixes rich language log level (RHBZ#993740)
  - fixes typo in firewall-cmd man page (RHBZ#1064401)
- new support to save runtime as permanent (RHBZ#993650)
- new cli --timeout time specifiers support (RHBZ#994044)
- updated translations (RHBZ#1048119) (RHBZ#1083592)
- more descriptive error message in case of mistakes in iptables (RHBZ#1057095)
- use apparent name for default target (RHBZ#1075675)
- simplified firewalld usage on servers by dropping at_console (RHBZ#1097765)
- fixed enable/disable of lockdown (RHBZ#1111573)
- new Satellite 6 service (RHBZ#1135634)
- fixed inconsistent color usage for firewall-cmd messages (RHBZ#1097841)
- fixed missing -Es in lockdown whitelist firewall-config command (RHBZ#1099065)
- unified runtime and permanent D-Bus API (RHBZ#1127706)
- fixed missing update of the connections menu in firewall-config (RHBZ#1120212)
- better docs for interface bindings in firewalld and NetworkManager (RHBZ#1112742)
- firewall-config: Show target REJECT (RHBZ#1058794)
- fixed inconsistent PolicyKit domain usage in main D-Bus interface (RHBZ#1061809)

* Fri Feb 28 2014 Jiri Popelka <jpopelka@redhat.com> - 0.3.9-7
- firewall-cmd: prevent argparse from parsing iptables options (RHBZ#1070683)

* Wed Feb 26 2014 Jiri Popelka <jpopelka@redhat.com> - 0.3.9-6
- firewall-offline-cmd: options from 'firewall-cmd --permanent *' (RHBZ#1059800)

* Sun Feb 23 2014 Thomas Woerner <twoerner@redhat.com> - 0.3.9-5
- fixed rich language log level (RHBZ#993740)
- firewall-config: use simple tool to change zones for connections (RHBZ#993782)
- translations update (RHBZ#1030330)
- firewall-config: fixed service and icmptype name dulications (RHBZ#1067639)
- allow router advertisements for IPv6 rpfilter (RHBZ#1067652)
- firewall-applet: allow to bind connections to the defaut zone (RHBZ#1068148)

* Wed Feb 12 2014 Thomas Woerner <twoerner@redhat.com> - 0.3.9-4
- firewall-config creates unloadable config; port forwarding broken
  (RHBZ#1057628)
- Network connection is lost after changing Zones Default Target to DROP
  (RHBZ#1057629)
- permanently adding rich rule with audit creates unloadable config XML
  (RHBZ#1057684)
- firewalld input_zones has default rule for public zone (RHBZ#1058339)
- firewall-cmd is not able to add and remove zones, services and icmptypes
  (RHBZ#1064386)
- firewall-config leaves deleted services shown if they were in use
  (RHBZ#1058853)
- firewall-cmd does not allow user to change zone default target (RHBZ#1058791)
- firewall-cmd man page has a typo in --help description (RHBZ#1064401)

* Fri Jan 17 2014 Thomas Woerner <twoerner@redhat.com> - 0.3.9-3
- fixed enforcing of trusted, drop and block zones (RHBZ#1054415)

* Thu Jan 16 2014 Thomas Woerner <twoerner@redhat.com> - 0.3.9-2
- fixed rich rules (RHBZ#1054270)
- fixed small defects in firewall-cmd and firewall-config (RHBZ#1054289)

* Wed Jan 15 2014 Thomas Woerner <twoerner@redhat.com> - 0.3.9-1
- rebase to 0.3.9 version:
- translation updates
- New IPv6_rpfilter setting to enable source address validation (RHBZ#847707)
- Do not mix original and customized zones in case of target changes,
  apply only used zones
- firewall-cmd: fix --*_lockdown_whitelist_uid to work with uid 0
- Don't show main window maximized. (RHBZ#1046811)
- Use rmmod instead of 'modprobe -r' (RHBZ#1031102)
- Deprecate 'enabled' attribute of 'masquerade' element
- firewall-config: new zone was added twice to the list
- firewalld.dbus(5)
- Enable python shebang fix again
- firewall/client: handle_exceptions: Use loop in decorator
- firewall-offline-cmd: Do not mask firewalld service with disabled option
- firewall-config: richRuleDialogActionRejectType Entry -> ComboBox
- Rich_Rule: fix parsing of reject element (RHBZ#1027373)
- Show combined zones in permanent configuration (RHBZ#1002016)
- firewall-cmd(1): document exit code 2 and colored output (RHBZ#1028507)
- firewall-config: fix RHBZ#1028853

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.3.8-2
- Mass rebuild 2013-12-27

* Tue Nov 05 2013 Jiri Popelka <jpopelka@redhat.com> - 0.3.8-1
- fix memory leaks
- New option --debug-gc
- Python3 compatibility
- Better non-ascii support
- several firewall-config & firewall-applet fixes
- New --remove-rules commands for firewall-cmd and removeRules methods for D-Bus
- Fixed FirewallDirect.get_rules to return proper list
- Fixed LastUpdatedOrderedDict.keys()
- Enable rich rule usage in trusted zone (RHBZ#994144)
- New error codes: INVALID_CONTEXT, INVALID_COMMAND, INVALID_USER and INVALID_UID

* Thu Oct 17 2013 Jiri Popelka <jpopelka@redhat.com> - 0.3.7-1
- Don't fail on missing ip[6]tables/ebtables table. (RHBZ#967376)
- bash-completion: --permanent --direct options
- firewall/core/fw.py: fix checking for iptables & ip6tables (RHBZ#1017087)
- firewall-cmd: use client's exception_handler instead of catching exceptions ourselves
- FirewallClientZoneSettings: fix {add|remove|query}RichRule()
- Extend amanda-client service with 10080/tcp (RHBZ#1016867)
- Simplify Rich_Rule()_lexer() by using functions.splitArgs()
- Fix encoding problems in exception handling (RHBZ#1015941)

* Fri Oct 04 2013 Jiri Popelka <jpopelka@redhat.com> - 0.3.6.2-1
- firewall-offline-cmd: --forward-port 'toaddr' is optional (RHBZ#1014958)
- firewall-cmd: fix variable name (RHBZ#1015011)

* Thu Oct 03 2013 Jiri Popelka <jpopelka@redhat.com> - 0.3.6.1-1
- remove superfluous po files from archive

* Wed Oct 02 2013 Jiri Popelka <jpopelka@redhat.com> - 0.3.6-1
- firewalld.richlanguage.xml: correct log levels (RHBZ#993740)
- firewall-config: Make sure that all zone settings are updated properly on firewalld restart
- Rich_Limit: Allow long representation for duration (RHBZ#994103
- firewall-config: Show "Changes applied." after changes (RHBZ#993643)
- Use own connection dialog to change zones for NM connections
- Rename service cluster-suite to high-availability (RHBZ#885257)
- Permanent direct support for firewall-config and firewall-cmd
- Try to avoid file descriptor leaking (RHBZ#951900)
- New functions to split and join args properly (honoring quotes)
- firewall-cmd(1): 2 simple examples
- Better IPv6 NAT checking.
- Ship firewalld.direct(5).

* Mon Sep 30 2013 Jiri Popelka <jpopelka@redhat.com> - 0.3.5-1
- Only use one PK action for configuration (RHBZ#994729)
- firewall-cmd: indicate non-zero exit code with red color
- rich-rule: enable to have log without prefix & log_level & limit
- log-level warn/err -> warning/error (RHBZ#1009436)
- Use policy DROP while reloading, do not reset policy in restart twice
- Add _direct chains to all table and chain combinations
- documentation improvements
- New firewalld.direct(5) man page docbook source
- tests/firewall-cmd_test.sh: make rich language tests work
- Rich_Rule._import_from_string(): improve error messages (RHBZ#994150)
- direct.passthrough wasn't always matching out_signature (RHBZ#967800)
- firewall-config: twist ICMP Type IP address family logic.
- firewall-config: port-forwarding/masquerading dialog (RHBZ#993658)
- firewall-offline-cmd: New --remove-service=<service> option (BZ#969106)
- firewall-config: Options->Lockdown was not changing permanent.
- firewall-config: edit line on doubleclick (RHBZ#993572)
- firewall-config: System Default Zone -> Default Zone (RHBZ#993811)
- New direct D-Bus interface, persistent direct rule handling, enabled passthough
- src/firewall-cmd: Fixed help output to use more visual parameters
- src/firewall-cmd: New usage output, no redirection to man page anymore
- src/firewall/core/rich.py: Fixed forwad port destinations
- src/firewall-offline-cmd: Early enable/disable handling now with mask/unmask
- doc/xml/firewalld.zone.xml: Added more information about masquerade use
- Prefix to log message is optional (RHBZ#998079)
- firewall-cmd: fix --permanent --change-interface (RHBZ#997974)
- Sort zones/interfaces/service/icmptypes on output.
- wbem-https service (RHBZ#996668)
- applet&config: add support for KDE NetworkManager connection editor
- firewall/core/fw_config.py: New method update_lockdown_whitelist
- Added missing file watcher for lockdown whitelist in config D-Bus interface
- firewall/core/watcher: New add_watch_file for lockdown-whitelist and direct
- Make use of IPv6 NAT conditional, based on kernel number (RHBZ#967376)

* Tue Jul 30 2013 Thomas Woerner <twoerner@redhat.com> 0.3.4-1
- several rich rule check enhancements and fixes
- firewall-cmd: direct options - check ipv4|ipv6|eb (RHBZ#970505)
- firewall-cmd(1): improve description of direct options (RHBZ#970509)
- several firewall-applet enhancements and fixes
- New README
- several doc and man page fixes
- Service definitions for PCP daemons (RHBZ#972262)
- bash-completion: add lockdown and rich language options
- firewall-cmd: add --permanent --list-all[-zones]
- firewall-cmd: new -q/--quiet option
- firewall-cmd: warn when default zone not active (RHBZ#971843)
- firewall-cmd: check priority in --add-rule (RHBZ#914955)
- add dhcpv6 (for server) service (RHBZ#917866)
- firewall-cmd: add --permanent --get-zone-of-interface/source --change-interface/source
- firewall-cmd: print result (yes/no) of all --query-* commands
- move permanent-getZoneOf{Interface|Source} from firewall-cmd to server
- Check Interfaces/sources when updating permanent zone settings.
- FirewallDConfig: getZoneOfInterface/Source can actually return more zones
- Fixed toaddr check in forward port to only allow single address, no range
- firewall-cmd: various output improvements
- fw_zone: use check_single_address from firewall.functions
- getZoneOfInterface/Source does not need to throw exception
- firewall.functions: Use socket.inet_pton in checkIP, fixed checkIP*nMask
- firewall.core.io.service: Properly check port/proto and destination address
- Install applet desktop file into /etc/xdg/autostart
- Fixed option problem with rich rule destinations (RHBZ#979804)
- Better exception creation in dbus_handle_exceptions() decorator (RHBZ#979790)
- Updated firewall-offline-cmd
- Use priority in add, remove, query and list of direct rules (RHBZ#979509)
- New documentation (man pages are created from docbook sources)
- firewall/core/io/direct.py: use prirority for rule methods, new get_all_ methods
- direct: pass priority also to client.py and firewall-cmd
- applet: New blink and blink-count settings
- firewall.functions: New function ppid_of_pid
- applet: Check for gnome3 and fix it, use new settings, new size-changed cb
- firewall-offline-cmd: Fix use of systemctl in chroot
- firewall-config: use string.ascii_letters instead of string.letters
- dbus_to_python(): handle non-ascii chars in dbus.String.
- Modernize old syntax constructions.
- dict.keys() in Python 3 returns a "view" instead of list
- Use gettext.install() to install _() in builtins namespace.
- Allow non-ascii chars in 'short' and 'description'
- README: More information for "Working With The Source Repository"
- Build environment fixes
- firewalld.spec: Added missing checks for rhel > 6 for pygobject3-base
- firewall-applet: New setting show-inactive
- Don't stop on reload when lockdown already enabled (RHBZ#987403)
- firewall-cmd: --lockdown-on/off did not touch firewalld.conf
- FirewallApplet.gschema.xml: Dropped unused sender-info setting
- doc/firewall-applet.xml: Added information about gsettings
- several debug and log message fixes
- Add chain for sources so they can be checked before interfaces (RHBZ#903222)
- Add dhcp and proxy-dhcp services (RHBZ#986947)
- io/Zone(): don't error on deprecated family attr of source elem
- Limit length of zone file name (to 12 chars) due to Netfilter internals.
- It was not possible to overload a zone with defined source(s).
- DEFAULT_ZONE_TARGET: {chain}_ZONE_{zone} -> {chain}_{zone}
- New runtime get<X>Settings for services and icmptypes, fixed policies callbacks
- functions: New functions checkUser, checkUid and checkCommand
- src/firewall/client: Fixed lockdown-whitelist-updated signal handling
- firewall-cmd(1): move firewalld.richlanguage(5) reference in --*-rich-rule
- Rich rule service: Only add modules for accept action
- firewall/core/rich: Several fixes and enhanced checks
- Fixed reload of direct rules
- firewall/client: New functions to set and get the exception handler
- firewall-config: New and enhanced UI to handle lockdown and rich rules
- zone's immutable attribute is redundant
- Do not allow to set settings in config for immutable zones.
- Ignore deprecated 'immutable' attribute in zone files.
- Eviscerate 'immutable' completely.
- FirewallDirect.query_rule(): fix it
- permanent direct: activate firewall.core.io.direct:Direct reader
- core/io/*: simplify getting of character data
- FirewallDirect.set_config(): allow reloading

* Thu Jun 20 2013  Jiri Popelka <jpopelka@redhat.com>
- Remove migrating to a systemd unit file from a SysV initscript
- Remove pointless "ExclusiveOS" tag

* Fri Jun  7 2013 Thomas Woerner <twoerner@redhat.com> 0.3.3-2
- Fixed rich rule check for use in D-Bus

* Thu Jun  6 2013 Thomas Woerner <twoerner@redhat.com> 0.3.3-1
- new service files
- relicensed logger.py under GPLv2+
- firewall-config: sometimes we don't want to use client's exception handler
- When removing Service/IcmpType remove it from zones too (RHBZ#958401)
- firewall-config: work-around masquerade_check_cb() being called more times
- Zone(IO): add interfaces/sources to D-Bus signature
- Added missing UNKNOWN_SOURCE error code
- fw_zone.check_source: Raise INVALID_FAMILY if family is invalid
- New changeZoneOfInterface method, marked changeZone as deprecated
- Fixed firewall-cmd man page entry for --panic-on
- firewall-applet: Fixed possible problems of unescaped strings used for markup
- New support to bind zones to source addresses and ranges (D-BUS, cmd, applet
- Cleanup of unused variables in FirewallD.start
- New firewall/fw_types.py with LastUpdatedOrderedDict
- direct.chains, direct.rules: Using LastUpdatedOrderedDict
- Support splitted zone files
- New reader and writer for stored direct chains and rules
- LockdownWhitelist: fix write(), add get_commands/uids/users/contexts()
- fix service_writer() and icmptype_writer() to put newline at end of file
- firewall-cmd: fix --list-sources
- No need to specify whether source address family is IPv4 or IPv6
- add getZoneOfSource() to D-Bus interface
- Add tests and bash-completion for the new "source" operations
- Convert all input args in D-Bus methods
- setDefaultZone() was calling accessCheck() *after* the action
- New uniqify() function to remove duplicates from list whilst preserving order
- Zone.combine() merge also services and ports
- config/applet: silence DBusException during start when FirewallD is not running (RHBZ#966518)
- firewall-applet: more fixes to make the address sources family agnostic
- Better defaults for lockdown white list
- Use auth_admin_keep for allow_any and allow_inactive also
- New D-Bus API for lockdown policies
- Use IPv4, IPv6 and BRIDGE for FirewallD properties
- Use rich rule action as audit type
- Prototype of string-only D-Bus interface for rich language
- Fixed wrongly merged source family check in firewall/core/io/zone.py
- handle_cmr: report errors, cleanup modules in error case only, mark handling
- Use audit type from rule action, fixed rule output
- Fixed lockdown whitelist D-Bus handling method names
- New rich rule handling in runtime D-Bus interface
- Added interface, source and rich rule handling (runtime and permanent)
- Fixed dbus_obj in FirewallClientConfigPolicies, added queryLockdown
- Write changes in setLockdownWhitelist
- Fixed typo in policies log message in method calls
- firewall-cmd: Added rich rule, lockdown and lockdown whitelist handling
- Don't check access in query/getLockdownWhitelist*()
- firewall-cmd: Also output masquerade flag in --list-all
- firewall-cmd: argparse is able to convert argument to desired type itself
- firewall-cmd_test.sh: tests for permanent interfaces/sources and lockdown whitelist
- Makefile.am: add missing files
- firewall-cmd_test.sh: tests for rich rules
- Added lockdown, source, interface and rich rule docs to firewall-cmd
- Do not masquerade lo if masquerade is enabled in the default zone (RHBZ#904098)
- Use <rule> in metavar for firewall-cmd parser

* Fri May 10 2013 Jiri Popelka <jpopelka@redhat.com> - 0.3.2-2
- removed unintentional en_US.po from tarball

* Tue Apr 30 2013 Jiri Popelka <jpopelka@redhat.com> - 0.3.2-1
- Fix signal handling for SIGTERM
- Additional service files (RHBZ#914859)
- Updated po files
- s/persistent/permanent/ (Trac Ticket #7)
- Better behaviour when running without valid DISPLAY (RHBZ#955414)
- client.handle_exceptions(): do not loop forever
- Set Zone.defaults in zone_reader (RHBZ#951747)
- client: do not pass the dbus exception name to handler
- IO_Object_XMLGenerator: make it work with Python 2.7.4 (RHBZ#951741)
- firewall-cmd: do not use deprecated BaseException.message
- client.py: fix handle_exceptions() (RHBZ#951314)
- firewall-config: check zone/service/icmptype name (RHBZ#947820)
- Allow 3121/tcp (pacemaker_remote) in cluster-suite service. (RHBZ#885257)
- firewall-applet: fix default zone hangling in 'shields-up' (RHBZ#947230)
- FirewallError.get_code(): check for unknown error

* Wed Apr 17 2013 Jiri Popelka <jpopelka@redhat.com> - 0.3.1-2
- Make permanenent changes work with Python 2.7.4 (RHBZ#951741)

* Thu Mar 28 2013 Thomas Woerner <twoerner@redhat.com> 0.3.1-1
- Use explicit file lists for make dist
- New rich rule validation check code
- New global check_port and check_address functions
- Allow source white and black listing with the rich rule
- Fix error handling in case of unsupported family in rich rule
- Enable ip_forwarding in masquerade and forward-port
- New functions to read and write simple files using filename and content
- Add --enable-sysconfig to install Fedora-specific sysconfig config file.
- Add chains for security table (RHBZ#927015)
- firewalld.spec: no need to specify --with-systemd-unitdir
- firewalld.service: remove syslog.target and dbus.target
- firewalld.service: replace hard-coded paths
- Move bash-completion to new location.
- Revert "Added configure for new build env"
- Revert "Added Makefile.in files"
- Revert "Added po/Makefile.in.in"
- Revert "Added po/LINGUAS"
- Revert "Added aclocal.m4"
- Amend zone XML Schema

* Wed Mar 20 2013 Thomas Woerner <twoerner@redhat.com> 0.3.0-1
- Added rich language support
- Added lockdown feature
- Allow to bind interfaces and sources to zones permanently
- Enabled IPv6 NAT support
  masquerading and port/packet forwarding for IPv6 only with rich language
- Handle polkit errors in client class and firewall-config
- Added priority description for --direct --add-rule in firewall-cmd man page
- Add XML Schemas for zones/services/icmptypes XMLs
- Don't keep file descriptors open when forking
- Introduce --nopid option for firewalld
- New FORWARD_IN_ZONES and FORWARD_OUT_ZONES chains (RHBZ#912782)
- Update cluster-suite service (RHBZ#885257)
- firewall-cmd: rename --enable/disable-panic to --panic-on/off (RHBZ#874912)
- Fix interaction problem of changed event of gtk combobox with polkit-kde
  by processing all remaining events (RHBZ#915892)
- Stop default zone rules being applied to all zones (RHBZ#912782)
- Firewall.start(): don't call set_default_zone()
- Add wiki's URL to firewalld(1) and firewall-cmd(1) man pages
- firewalld-cmd: make --state verbose (RHBZ#886484)
- improve firewalld --help (RHBZ#910492)
- firewall-cmd: --add/remove-* can be used multiple times (RHBZ#879834)
- Continue loading zone in case of wrong service/port etc. (RHBZ#909466)
- Check also services and icmptypes in Zone() (RHBZ#909466)
- Increase the maximum length of the port forwarding fields from 5 to 11 in
  firewall-config
- firewall-cmd: add usage to fail message
- firewall-cmd: redefine usage to point to man page
- firewall-cmd: fix visible problems with arg. parsing
- Use argparse module for parsing command line options and arguments
- firewall-cmd.1: better clarify where to find ACTIONs
- firewall-cmd Bash completion
- firewall-cmd.1: comment --zone=<zone> usage and move some options
- Use zone's target only in %s_ZONES chains
- default zone in firewalld.conf was set to public with every restart (#902845)
- man page cleanup
- code cleanup

* Thu Mar 07 2013 Jiri Popelka <jpopelka@redhat.com> - 0.2.12-5
- Another fix for RHBZ#912782

* Wed Feb 20 2013 Jiri Popelka <jpopelka@redhat.com> - 0.2.12-4
- Stop default zone rules being applied to all zones (RHBZ#912782)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Jiri Popelka <jpopelka@redhat.com> - 0.2.12-2
- Default zone in firewalld.conf was reseted with every restart (RHBZ#902845)
- Add icon cache related scriptlets for firewall-config (RHBZ#902680)
- Fix typo in firewall-config (RHBZ#895812)
- Fix few mistakes in firewall-cmd(1) man page

* Mon Jan 14 2013 Thomas Woerner <twoerner@redhat.com> 0.2.12-1
- firewall-cmd: use -V instead of -v for version info (RHBZ#886477)
- firewall-cmd: don't check reload()'s return value (RHBZ#886461)
- actually install firewalld.zones.5
- firewall-config: treat exceptions when adding new zone/service/icmp
  (RHBZ#886602)
- firewalld.spec: Fixed requirements of firewall-config to use gtk2 and
  pygobject3
- Fail gracefully when running in non X environment.(RHBZ#886551)
- offline-cmd: fail gracefully when no s-c-f config
- fix duplicated iptables rules (RHBZ#886515)
- detect errors and duplicates in config file (RHBZ#886581)
- firewall-config: don't make 'Edit Service' and 'Edit ICMP Type' insensitive
- firewalld.spec: fixed requirements, require pygobject3-base
- frewall-applet: Unused code cleanup
- firewall-applet: several usability fixes and enhancements
  (RHBZ#886531) (RHBZ#886534)
- firewall/server/server.py: fixed KeyboardInterrupt message (RHBZ#886558)
- Moved fallback zone and minimal_mark to firewall.config.__init__
- Do not raise ZONE_ALREADY_SET in change_zone if old zone is set again
  (RHBZ#886432)
- Make default zone default for all unset connections/interfaces
  (RHBZ#888288) (RHBZ#882736)
- firewall-config: Use Gtk.MessageType.WARNING for warning dialog
- firewall-config: Handle unknown services and icmptypes in persistent mode
- firewall-config: Do not load settings more than once
- firewall-config: UI cleanup and fixes (RHBZ#888242)
- firewall-cmd: created alias --change-zone for --change-interface
- firewall-cmd man page updates (RHBZ#806511)
- Merged branch 'build-cleanups'
- dropped call to autogen.sh in build stage, not needed anymore due to 
  'build-cleanups' merge

* Thu Dec 13 2012 Thomas Woerner <twoerner@redhat.com> 0.2.11-2
- require pygobject3-base instead of pygobject3 (no cairo needed) (RHBZ#874378)
- fixed dependencies of firewall-config to use gtk3 with pygobject3-base and 
  not pygtk2

* Tue Dec 11 2012 Thomas Woerner <twoerner@redhat.com> 0.2.11-1
- Fixed more _xmlplus (PyXML) incompatibilities to python xml
- Several man page updates
- Fixed error in addForwardPort, removeForwardPort and queryForwardPort
- firewall-cmd: use already existing queryForwardPort()
- Update firewall.cmd man page, use man page as firewall-cmd usage (rhbz#876394)
- firewall-config: Do not force to show labels in the main toolbar
- firewall-config: Dropped "Change default zone" from toolbar
- firewall-config: Added menu entry to change zones of connections
- firewall-applet: Zones can be changed now using nm-connection-editor
  (rhbz#876661)
- translation updates: cs, hu, ja

* Tue Nov 20 2012 Thomas Woerner <twoerner@redhat.com> 0.2.10-1
- tests/firewalld_config.py: tests for config.service and config.icmptype
- FirewallClientConfigServiceSettings(): destinations are dict not list
- service/zone/icmptype: do not write deprecated name attribute
- New service ntp
- firewall-config: Fixed name of about dialog
- configure.in: Fixed getting of error codes
- Added coding to all pyhton files
- Fixed copyright years
- Beautified file headers
- Force use of pygobject3 in python-slip (RHBZ#874378)
- Log: firewall.server.config_icmptype, firewall.server.config_service and
  firewall.server.config_zone: Prepend full path
- Allow ":" in interface names for interface aliases
- Add name argument to Updated and Renamed signal
- Disable IPv4, IPv6 and EB tables if missing - for IPv4/IPv6 only environments
- firewall-config.glade file cleanup
- firewall-config: loadDefaults() can throw exception
- Use toolbars for Add/Edit/Remove/LoadDefaults buttons for zones, services
  and icmp types
- New vnc-server service, opens ports for displays :0 to :3 (RHBZ#877035)
- firewall-cmd: Fix typo in help output, allow default zone usage for
  permanenent options
- Translation updates: cs, fr, ja, pt_BR and zh_CN

* Wed Oct 17 2012 Thomas Woerner <twoerner@redhat.com> 0.2.9-1
- firewall-config: some UI usability changes
- firewall-cmd: New option --list-all-zones, output of --list-all changed,
  more option combination checks
- firewall-applet: Replaced NMClient by direct DBUS calls to fix python core
  dumps in case of connection activates/deactivates
- Use fallback 'C' locale if current locale isn't supported (RHBZ#860278)
- Add interfaces to zones again after reload
- firewall-cmd: use FirewallClient().connected value
- firewall-cmd: --remove-interface was not working due to a typo
- Do not use restorecon for new and backup files
- Fixed use of properties REJECT and DROP
- firewalld_test.py: check interfaces after reload
- Translation updates
- Renamed firewall-convert-scfw-config to firewall-offline-cmd, used by
  anaconda for firewall configuration (e.g. kickstart)
- Fix python shebang to use -Es at installation time for bin_SCRIPTS and
  sbin_SCRIPTS and at all times in gtk3_chooserbutton.py
- tests/firewalld_config.py: update test_zones() test case
- Config interface: improve renaming of zones/services/icmp_types
- Move emiting of Added signals closer to source.
- FirewallClient(): config:ServiceAdded signal was wrongly mapped
- Add argument 'name' to Removed signal
- firewall-config: Add callbacks for config:[service|icmp]-[added|removed]
- firewall-config: catch INVALID_X error when removing zone/service/icmp_type
- firewall-config: remove unused code
- Revert "Neutralize _xmlplus instead of conforming it"
- firewall-applet: some UI usability changes
- firewall-cmd: ALREADY_ENABLED, NOT_ENABLED, ZONE_ALREADY_SET are warnings

* Fri Sep  7 2012 Thomas Woerner <twoerner@redhat.com> 0.2.8-1
- Do not apply old settings to zones after reload
- FirewallClient: Added callback structure for firewalld signals
- New firewall-config with full zone, service and icmptype support
- Added Shields Up/Down configuration dialog to firewall-applet
- Name attribute of main tag deprecated for zones, services and icmptypes,
  will be ignored if present
- Fixed wrong references in firewalld man page
- Unregister DBus interfaces after sending out the Removed signal
- Use proper DBus signature in addIcmpType, addService and addZone
- New builtin property for config interfaces
- New test case for Config interface
- spec: use new systemd-rpm macros (rhbz#850110)
- More config file verifications
- Lots of smaller fixes and enhancements

* Tue Aug 21 2012 Jiri Popelka <jpopelka@redhat.com> 0.2.7-2
- use new systemd-rpm macros (rhbz#850110)

* Mon Aug 13 2012 Thomas Woerner <twoerner@redhat.com> 0.2.7-1
- Update of firewall-config
- Some bug fixes

* Tue Aug  7 2012 Thomas Woerner <twoerner@redhat.com> 0.2.6-1
- New D-BUS interface for persistent configuration
- Aded support for persistent zone configuration in firewall-cmd
- New Shields Up feature in firewall-applet
- New requirements for python-decorator and pygobject3
- New firewall-config sub-package
- New firewall-convert-scfw-config config script

* Fri Apr 20 2012 Thomas Woerner <twoerner@redhat.com> 0.2.5-1
- Fixed traceback in firewall-cmd for failed or canceled authorization, 
  return proper error codes, new error codes NOT_RUNNING and NOT_AUTHORIZED
- Enhanced firewalld service file (RHBZ#806868) and (RHBZ#811240)
- Fixed duplicates in zone after reload, enabled timed settings after reload
- Removed conntrack --ctstate INVALID check from default ruleset, because it
  results in ICMP problems (RHBZ#806017).
- Update interfaces in default zone after reload (rhbz#804814)
- New man pages for firewalld(1), firewalld.conf(5), firewalld.icmptype(5),
  firewalld.service(5) and firewalld.zone(5), updated firewall-cmd man page
  (RHBZ#811257)
- Fixed firewall-cmd help output
- Fixed missing icon for firewall-applet (RHBZ#808759)
- Added root user check for firewalld (RHBZ#767654)
- Fixed requirements of firewall-applet sub package (RHBZ#808746)
- Update interfaces in default zone after changing of default zone (RHBZ#804814)
- Start firewalld before NetworkManager (RHBZ#811240)
- Add Type=dbus and BusName to service file (RHBZ#811240)

* Fri Mar 16 2012 Thomas Woerner <twoerner@redhat.com> 0.2.4-1
- fixed firewalld.conf save exception if no temporary file can be written to 
  /etc/firewalld/

* Thu Mar 15 2012 Thomas Woerner <twoerner@redhat.com> 0.2.3-1
- firewall-cmd: several changes and fixes
- code cleanup
- fixed icmp protocol used for ipv6 (rhbz#801182)
- added and fixed some comments
- properly restore zone settings, timeout is always set, check for 0
- some FirewallError exceptions were actually not raised
- do not REJECT in each zone
- removeInterface() don't require zone
- new tests in firewall-test script
- dbus_to_python() was ignoring certain values
- added functions for the direct interface: chains, rules, passthrough
- fixed inconsistent data after reload
- some fixes for the direct interface: priority positions are bound to ipv,
  table and chain
- added support for direct interface in firewall-cmd:
- added isImmutable(zone) to zone D-Bus interface
- renamed policy file
- enhancements for error messages, enables output for direct.passthrough
- added allow_any to firewald policies, using at leas auth_admin for policies
- replaced ENABLE_FAILED, DISABLE_FAILED, ADD_FAILED and REMOVE_FAILED by
  COMMAND_FAILED, resorted error codes
- new firewalld configuration setting CleanupOnExit
- enabled polkit again, found a fix for property problem with slip.dbus.service
- added dhcpv6-client to 'public' (the default) and to 'internal' zones.
- fixed missing settings form zone config files in
  "firewall-cmd --list=all --zone=<zone>" call
- added list functions for services and icmptypes, added --list=services and
  --list=icmptypes to firewall-cmd

* Tue Mar  6 2012 Thomas Woerner <twoerner@redhat.com> 0.2.2-1
- enabled dhcpv6-client service for zones home and work
- new dhcpv6-client service
- firewall-cmd: query mode returns reversed values
- new zone.changeZone(zone, interface)
- moved zones, services and icmptypes to /usr/lib/firewalld, can be overloaded
  by files in /etc/firewalld (no overload of immutable zones block, drop,
  trusted)
- reset MinimalMark in firewalld.cnf to default value
- fixed service destination (addresses not used)
- fix xmlplus to be compatible with the python xml sax parser and python 3
  by adding __contains__ to xml.sax.xmlreader.AttributesImpl
- use icon and glib related post, postun and posttrans scriptes for firewall
- firewall-cmd: fix typo in state
- firewall-cmd: fix usage()
- firewall-cmd: fix interface action description in usage()
- client.py: fix definition of queryInterface()
- client.py: fix typo in getInterfaces()
- firewalld.service: do not fork
- firewall-cmd: fix bug in --list=port and --port action help message
- firewall-cmd: fix bug in --list=service

* Mon Mar  5 2012 Thomas Woerner <twoerner@redhat.com>
- moved zones, services and icmptypes to /usr/lib/firewalld, can be overloaded
  by files in /etc/firewalld (no overload of immutable zones block, drop,
  trusted)

* Tue Feb 21 2012 Thomas Woerner <twoerner@redhat.com> 0.2.1-1
- added missing firewall.dbus_utils

* Tue Feb  7 2012 Thomas Woerner <twoerner@redhat.com> 0.2.0-2
- added glib2-devel to build requires, needed for gsettings.m4
- added --with-system-unitdir arg to fix installaiton of system file
- added glib-compile-schemas calls for postun and posttrans
- added EXTRA_DIST file lists

* Mon Feb  6 2012 Thomas Woerner <twoerner@redhat.com> 0.2.0-1
- version 0.2.0 with new FirewallD1 D-BUS interface
- supports zones with a default zone
- new direct interface as a replacement of the partial virt interface with 
  additional passthrough functionality
- dropped custom rules, use direct interface instead
- dropped trusted interface funcionality, use trusted zone instead
- using zone, service and icmptype configuration files
- not using any system-config-firewall parts anymore

* Mon Feb 14 2011 Thomas Woerner <twoerner@redhat.com> 0.1.3-1
- new version 0.1.3
- restore all firewall features for reload: panic and virt rules and chains
- string fixes for firewall-cmd man page (by Jiri Popelka)
- fixed firewall-cmd port list (by Jiri Popelka)
- added firewall dbus client connect check to firewall-cmd (by Jiri Popelka)
- translation updates: de, es, gu, it, ja, kn, ml, nl, or, pa, pl, ru, ta,
                       uk, zh_CN

* Mon Jan  3 2011 Thomas Woerner <twoerner@redhat.com> 0.1.2-1
- fixed package according to package review (rhbz#665395):
  - non executable scripts: dropped shebang
  - using newer GPL license file
  - made /etc/dbus-1/system.d/FirewallD.conf config(noreplace)
  - added requires(post) and (pre) for chkconfig

* Mon Jan  3 2011 Thomas Woerner <twoerner@redhat.com> 0.1.1-1
- new version 0.1.1
- fixed source path in POTFILES*
- added missing firewall_config.py.in
- added misssing space for spec_ver line
- using firewall_config.VARLOGFILE
- added date to logging output
- also log fatal and error logs to stderr and firewall_config.VARLOGFILE
- make log message for active_firewalld fatal

* Mon Dec 20 2010 Thomas Woerner <twoerner@redhat.com> 0.1-1
- initial package (proof of concept implementation)
