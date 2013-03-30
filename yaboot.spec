Summary: Linux bootloader for Power Macintosh "New World" computers
Name: yaboot
Version: 1.3.14
Release: 35%{?dist}.1
License: GPLv2+
Group: System Environment/Base
Source: http://yaboot.ozlabs.org/releases/yaboot-%{version}.tar.gz
Source1: efika.forth

# include various git patches that have been there
# Patches were included directly in tarball. This is not ok, because
# tarball was different then upstream. So do the changes in patch
Patch0: yaboot-1.3.14-gitpatches.patch

Patch1: yaboot-1.3.3-man.patch
Patch2: yaboot-1.3.6-ofboot.patch
Patch3: yaboot-1.3.6-rh.patch
Patch4: yaboot-1.3.13-yabootconfig.patch
Patch6: yaboot-1.3.10-proddiscover.patch
Patch7: yaboot-1.3.10-ext3.patch
Patch8: yaboot-1.3.10-sbindir.patch
Patch9: yaboot-1.3.10-configfile.patch
Patch10: yaboot-1.3.10-parted.patch
Patch17: yaboot-1.3.13-pegasos-claim.patch
Patch18: yaboot-1.3.13-pegasos-ext2.patch
Patch21: yaboot-1.3.13-pegasos-serial.patch
Patch22: yaboot-1.3.13-allow-deep-mntpoint.patch
Patch28: yaboot-1.3.13-dontwritehome.patch
Patch30: yaboot-1.3.14-fix-bootonce-nvram.patch 
Patch31: yaboot-1.3.14-bigger-max-token.patch
Patch32: yaboot-relocatable-kernel.patch
Patch33: yaboot-1.3.14-better_netboot.patch
Patch34: yaboot-1.3.14-no-birecs.patch

# mkofboot in verbose mode returns bad value
Patch35: yaboot-1.3.14-returns.patch

# ipv6 support
Patch36: yaboot-1.3.14-ipv6.patch

# Do not open LINUX_NATIVE parttions with OF, as badness happens
Patch37: yaboot-1.3.14-dont_of_open_native_partitions.patch

# Try #2 at better netboot now with DHCP parseing
Patch38: yaboot-1.3.14-better_netboot2.patch

# When netbooting, move the kernel onto the load buffer, sure it's a hack
Patch39: yaboot-1.3.14-move_kernel.patch

# SHA-2 support
Patch40: yaboot-sha2.patch

# Solves the situation, when there is no netinfo packet
Patch41: yaboot-1.3.14-netinfo.patch

# Better ISCSI boot
Patch42: yaboot-1.3.14-iscsi.patch

# prom_getchar eats characters
Patch43: yaboot-1.3.14-prom_getchars.patch

# Allow yaboot to allocate up to 256MB of memory
Patch44: yaboot-1.3.14-256-RMA.patch

# 621598, better memory management
Patch45: yaboot-1.3.14-memory_management.patch

# 638654, properly boot when gateway != tftp server
Patch46: yaboot-1.3.14-subnetmask.patch

URL: http://yaboot.ozlabs.org/
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
ExclusiveArch: ppc

# hfsutils will not be in RHEL6.
# hfsutils is needed only for non-IBM ppc machines
%if 0%{?fedora} || 0%{?rhel} < 6
Requires: hfsutils
%endif
BuildRequires: e2fsprogs-devel

# yaboot is bootloader. It contains ELF object, but it is not Linux or MacOS
# executable file. Yaboot is meant to be executed only by OpenFirmware.
# So debuginfo rpm is nonsense
%global debug_package %{nil}

%description
yaboot is a bootloader for PowerPC machines which works on New World ROM
machines (Rev. A iMac and newer) and runs directly from Open Firmware,
eliminating the need for Mac OS.
yaboot can also bootload IBM pSeries machines.

%prep
%setup -q
%patch0 -p1 -b .gitpatches
%patch1 -p0 -b .man
%patch2 -p1 -b .ofboot
%patch3 -p1 -b .rh
%patch4 -p1 -b .yabootconfig
%patch6 -p1 -b .proddisc
%patch7 -p1 -b .ext3
%patch8 -p1 -b .sbin
%patch9 -p1 -b .config
%patch10 -p1 -b .parted
%patch17 -p1 -b .pegasos
%patch18 -p1 -b .ext2
%patch21 -p1 -b .pegasos-serial
%patch22 -p1 -b .deepmnt
%patch28 -p1 -b .bootwrite
%patch30 -p1 -b .bootonce
%patch31 -p1 -b .maxtoken
%patch32 -p1 -b .relocatable
%patch33 -p1 -b .netboot
%patch34 -p1 -b .birecs
%patch35 -p1 -b .returns
%patch36 -p1 -b .ipv6
%patch37 -p1 -b .partitions
%patch38 -p1 -b .netboot2
%patch39 -p1 -b .movekernel
%patch40 -p1 -b .sha2
%patch41 -p1 -b .netinfo
%patch42 -p1 -b .iscsi
%patch43 -p1 -b .prom_getchars
%patch44 -p1 -b .256-RMA
%patch45 -p1 -b .memory_management
%patch46 -p1 -b .subnetmask

%build
iconv -f ISO88592 -t utf-8 -o doc/yaboot-howto.de.try.sgml \
  doc/yaboot-howto.de.sgml && mv -f doc/yaboot-howto.de.try.sgml \
  doc/yaboot-howto.de.sgml
make CFLAGS=-fno-strict-aliasing VERSIONEXTRA='\ (Red Hat %version-%release)' DEBUG=1
cp -a second/yaboot{,.debug}
make clean
make CFLAGS=-fno-strict-aliasing VERSIONEXTRA='\ (Red Hat %version-%release)'

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall ROOT=$RPM_BUILD_ROOT PREFIX=%{_prefix} MANDIR=share/man SBINDIR=/sbin
rm -f $RPM_BUILD_ROOT/etc/yaboot.conf
touch $RPM_BUILD_ROOT/etc/yaboot.conf
mkdir -p $RPM_BUILD_ROOT/boot
install -m0644 %{SOURCE1} $RPM_BUILD_ROOT/boot/efika.forth
install -m0644 second/yaboot.debug $RPM_BUILD_ROOT/usr/lib/yaboot/
rm -f $RPM_BUILD_ROOT/usr/share/doc/yaboot-1.3.14/README.man.patch
rm -f $RPM_BUILD_ROOT/usr/share/doc/yaboot-1.3.14/Makefile

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING README* doc/*
/boot/efika.forth
/sbin/ofpath
/sbin/ybin
/sbin/yabootconfig
/sbin/mkofboot
%dir /usr/lib/yaboot/
/usr/lib/yaboot/addnote
/usr/lib/yaboot/ofboot
/usr/lib/yaboot/yaboot
/usr/lib/yaboot/yaboot.debug
%{_mandir}/man8/bootstrap.8.gz
%{_mandir}/man8/mkofboot.8.gz
%{_mandir}/man8/ofpath.8.gz
%{_mandir}/man8/yaboot.8.gz
%{_mandir}/man8/yabootconfig.8.gz
%{_mandir}/man8/ybin.8.gz
%{_mandir}/man5/yaboot.conf.5.gz
%ghost %config(noreplace) %{_sysconfdir}/yaboot.conf

%changelog
* Wed Oct 13 2010 Roman Rakus <rrakus@redhat.com> - 1.3.14-35.1
- Properly load config file while netbooting and gateway != tftp server
  Resolves: #642694

* Fri Aug 06 2010 Roman Rakus <rrakus@redhat.com> - 1.3.14-35
- Better memory management
  Resolves: #621598

* Fri Jun 11 2010 Roman Rakus <rrakus@redhat.com> - 1.3.14-34
- Use -fno-strict-aliasing CFLAG and mark /usr/lib/yaboot as a dir in files
  section
  Resolves: #599403

* Wed May 26 2010 Roman Rakus <rrakus@redhat.com> - 1.3.14-33
- Allow yaboot to allocate up to 256MB of memory
  Resolves: #596299

* Wed May 26 2010 Roman Rakus <rrakus@redhat.com> - 1.3.14-32
- Get back #ExlusiveArch
  Resolves: #593377

* Wed May 26 2010 Roman Rakus <rrakus@redhat.com> - 1.3.14-31
- Allow copy&paste
  Resolves: #593377

* Tue Mar 18 2010 Roman Rakus <rrakus@redhat.com> - 1.3.14-30
- Better iSCSI booting
  Resolves: #553748

* Tue Mar 16 2010 Roman Rakus <rrakus@redhat.com> - 1.3.14-29
- Added missing yaboot-1.3.14-netinfo.patch
  Resolves: #553061

* Tue Mar 16 2010 Roman Rakus <rrakus@redhat.com> - 1.3.14-28
- Don't fail when there is no netinfo packet
  Resolves: #553061

* Fri Feb 26 2010 Roman Rakus <rrakus@redhat.com> - 1.3.14-27
- Update to include various changes from git that have been Fedora since .14
  was added.
- Don't end summary with dot.

* Fri Jan 22 2010 Roman Rakus rrakus@redhat.com 1.3.14-26
- SHA2 support
  Resolves: #555093

* Tue Jan 12 2010 rrakus@redhat.com 1.3.14-25
- Use correct upstream source tarball
- Patch changed for that source
  Resolves: #554676

* Tue Jan 12 2010 rrakus@redhat.com 1.3.14-24
- Fixed summary, buildroot
- Converted doc/yaboot-howto.de.sgml to utf8
- Clear buildroot before install
- Removed README.man.patch and Makefile from doc dir
- Own /usr/lib/yaboot/
- defattr(-,root,root,-)
  Resolves: #554676

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.3.14-23.1
- Rebuilt for RHEL 6

* Thu Oct 29 2009 Roman Rakus <rrakus@redhat.com> - 1.3.14-23
- When netbooting "clobber" the LOAD_BUFFER and move the kernel into it to make
  room for RTAS (#530330)
- Adding better netboot support more work on (#458438)

* Mon Oct 19 2009 Tony Breed <tony@bakeyournoodle.com> - 1.3.14-22
- Calling of_open() on a LINUX_NATIVE parttions seesm to work but end up with a
  garbage file.  Add check to of_open to skip these parttions (#526021).

* Mon Oct 19 2009 Tony Breed <tony@bakeyournoodle.com> - 1.3.14-21
- Explicitly build a DEBUG=1 version of yaboot to aid in debugging

* Mon Oct 19 2009 Tony Breed <tony@bakeyournoodle.com> - 1.3.14-20
- Only require hfsutils on fedora and rhel <= 5

* Thu Sep 09 2009 Roman Rakus <rrakus@redhat.com> - 1.3.14-19
- Increase TFTP buffer to 32MB

* Wed Sep 09 2009 Roman Rakus <rrakus@redhat.com> - 1.3.14-18
- Do not require hfsutils on RHEL 6

* Fri Aug 14 2009 Roman Rakus <rrakus@redhat.com> - 1.3.14-17
- ipv6 support
- don't build debuginfo package

* Fri Aug 07 2009 Bill Nottingham <notting@redhat.com> - 1.3.14-16
- fix patch file for (#515555)

* Fri Aug 07 2009 Roman Rakus <rrakus@redhat.com> - 1.3.14-15
- Fix bad return code in verbose mode (#515555)

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.14-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 07 2009 David Woodhouse <David.Woodhouse@intel.com> - 1.3.14-13
- Don't set up bi_recs. Especially not in the middle of the kernel text.

* Mon Apr 06 2009 tony@bakeyournoodle.com - 1.3.14-12
- Increase the TFTP load buffer from 20MiB to 25MiB. (#483051)

* Fri Mar 13 2009 tony@bakeyournoodle.com - 1.3.14-11
- Adding better netboot support (#458438)
- Allocate more buffer space for larger kernels and initrds (#472225)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.14-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Josh Boyer <jwboyer@gmail.com> - 1.3.14-9
- Add patch to handle relocatable kernels

* Thu Nov 27 2008 Roman Rakus <rrakus@redhat.com> - 1.3.14-8
- Bumped release, so preupgrade is now silent and go through

* Fri Nov 21 2008 David Woodhouse <David.Woodhouse@intel.com> - 1.3.14-7
- Fix 'ybin --bootonce' (#471425)
- Fix maximum token length, to fix preupgrade (#471321)

* Wed Nov 05 2008 Roman Rakus <rrakus@redhat.com> - 1.3.14-6
- Changed kernel load base address
  Resolves: #468492

* Mon Aug 11 2008 Roman Rakus <rrakus@redhat.com> - 1.3.14-5
- Clearing in specfile
- Fixed patches for --fuzz=0

* Wed May 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3.14-4
- fix license tag

* Wed Apr 16 2008 Roman Rakus <rrakus@redhat.com> - 1.3.14-3
- Upstream 1.3.14

* Thu Mar 27 2008 David Woodhouse <dwmw2@redhat.com> - 1.3.13-11
- Correct off-by-one error in Amiga partition numbers

* Thu Mar 27 2008 David Woodhouse <dwmw2@redhat.com> - 1.3.13-10
- Don't increment partition number to work around bplan firmware 
  brokenness when the config file was specified on the command line

* Fri Feb 08 2008 David Cantrell <dcantrell@redhat.com> - 1.3.13-9
- Rebuild for gcc-4.3

* Wed Nov 28 2007 David Woodhouse <dwmw2@redhat.com> - 1.3.13-8
- Correct default config file location on Efika
- Disable new USB bindings in efika.forth for now

* Tue Nov 27 2007 David Woodhouse <dwmw2@redhat.com> - 1.3.13-7
- Add efika.forth for fixing up Efika device-tree

* Tue Nov 27 2007 David Woodhouse <dwmw2@redhat.com> - 1.3.13-6
- Detect broken bplan firmware and don't add ":0" to block device names

* Tue Aug 21 2007 David Cantrell <dcantrell@redhat.com> - 1.3.13-5
- Rebuild

* Thu Nov 16 2006 Paul Nasrat <pnasrat@redhat.com> - 1.3.13-4
- Add support for usb/firewire from Alex Kanavin (#208768)

* Thu Nov 09 2006 Paul Nasrat <pnasrat@redhat.com> - 1.3.13-3
- Apply addnote patch (#184714)

* Wed Aug 23 2006 Paul Nasrat <pnasrat@redhat.com> - 1.3.13-2
- Fix ybin with SELinux (#201414)

* Mon Aug 21 2006 Paul Nasrat <pnasrat@redhat.com> - 1.3.13-1
- Fix multi disk G5 patch for all cases

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.3.13-0.18.1
- rebuild

* Tue Feb 21 2006 Paul Nasrat <pnasrat@redhat.com> - 1.3.13-0.18
- Drop telnet console patch for now (#182180)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.3.13-0.17.1
- bump again for double-long bug on ppc(64)

* Thu Feb 09 2006 Paul Nasrat <pnasrat@redhat.com> - 1.3.13-0.17
- Fix ofpath for multi-disk G5 (#180182)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.3.13-0.16.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Sep 14 2005 Jeremy Katz <katzj@redhat.com> - 1.3.13-0.16
- fix paths

* Wed Sep 14 2005 Jeremy Katz <katzj@redhat.com> - 1.3.13-0.15
- fix build on ppc64

* Wed Sep 14 2005 Paul Nasrat <pnasrat@redhat.com> - 1.3.13-0.14
- New netboot patch handling device=alias: for non network case

* Tue Sep 13 2005 David Woodhouse <dwmw2@redhat.com> - 1.3.13-0.13
- Print version-release of yaboot

* Mon Sep 12 2005 Paul Nasrat <pnasrat@redhat.com> - 1.3.13-0.12
- reworking of netboot patch (Nathan Lynch)

* Sat Aug 20 2005 Paul Nasrat <pnasrat@redhat.com> - 1.3.13-0.11
- drop netboot patch as mac cds fail to load yaboot.conf

* Wed Aug 17 2005 Paul Nasrat <pnasrat@redhat.com> - 1.3.13-0.10
- No colours on unsupported consoles (eg telnet)
- Improved pSeries netbooting (Nathan Lynch)

* Sun Aug 14 2005 David Woodhouse <dwmw2@redhat.com> - 1.3.13-0.9
- Try harder to allocate malloc region

* Thu Aug 11 2005 David Woodhouse <dwmw2@redhat.com> - 1.3.13-0.8
- Allow mntpoint to be more than one directory into the partition 
  as long as magicboot and nvram are not being used.

* Thu Aug 11 2005 David Woodhouse <dwmw2@redhat.com> - 1.3.13-0.7
- Fix error in swraid2 patch -- don't dereference NULL pointer.

* Tue Aug  9 2005 David Woodhouse <dwmw2@redhat.com> - 1.3.13-0.6
- Fix handling of prom 'read' method, to make Pegasos serial work

* Tue Aug  9 2005 David Woodhouse <dwmw2@redhat.com> - 1.3.13-0.5
- Fix Pegasos partition hack

* Tue Aug  9 2005 David Woodhouse <dwmw2@redhat.com> - 1.3.13-0.4
- Make default boot after timeout work again
- Pegasos disagrees about partition numbering

* Sat Jul 30 2005 David Woodhouse <dwmw2@redhat.com> - 1.3.13-0.3
- Accept config file path on command line
- Make ofpath work on Pegasos

* Fri Jul 29 2005 David Woodhouse <dwmw2@redhat.com> - 1.3.13-0.2
- Workaround claim bug in Pegasos SmartFirmware
- Handle ext2 boot partition

* Fri Jul 22 2005 Paul Nasrat <pnasrat@redhat.com> - 1.3.13-0.1
- Upstream 1.3.13
- Add patches on yaboot-1.3.x tree
- Try dropping ppc64 initrd patch

* Tue Mar 15 2005 Paul Nasrat <pnasrat@redhat.com> - 1.3.12-9
- GCC 4 rebuild

* Wed Feb 02 2005 Paul Nasrat <pnasrat@redhat.com> - 1.3.12-8
- addnote support for IBM,RPA-Client-Config note (#145739)
- Patch to recognise l-lan as a network device

* Wed Jul 28 2004 Paul Nasrat <pnasrat@redhat.com> - 1.3.12-7
- Add yaboot.conf as ghost

* Sat Jul 10 2004 Paul Nasrat <pnasrat@redhat.com> - 1.3.12-6
- Rebuild

* Sat Jul 10 2004 Paul Nasrat <pnasrat@redhat.com> - 1.3.12-5
- Added hfsutils requires for pmac

* Wed Jun 23 2004 David Woodhouse <dwmw2@redhat.com> - 1.3.12-4
- Increase TFTP load buffer size to 8MiB.

* Fri Jun 18 2004 Jeremy Katz <katzj@redhat.com> - 1.3.12-3
- s/Copyright/License/
- fix build with gcc 3.4

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 24 2004 Paul Nasrat <pnasrat@redhat.com> 1.3.12-1
- update to 1.3.12

* Tue Apr 20 2004 David Woodhouse <dwmw2@redhat.com> 1.3.10-10
- make yabootconfig use parted if available

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Aug 22 2003 Elliot Lee <sopwith@redhat.com> 1.3.10-8
- Build for rawhide

* Fri Jun 20 2003 Jeremy Katz <katzj@redhat.com> 1.3.10-7
- allow passing configfile name to yabootconfig with -C

* Wed Jun 18 2003 Jeremy Katz <katzj@redhat.com> 1.3.10-6
- don't ship (invalid) default yaboot.conf
- update to newer version of ppc64 initrd patch

* Mon Apr 28 2003 Jeremy Katz <katzj@redhat.com> 1.3.10-5
- clean up how yabootconfig adds stuff, do some rediff'ing
- install ybin, etc in /sbin instead of /usr/sbin (#83229)

* Wed Apr 23 2003 Jeremy Katz <katzj@redhat.com> 1.3.10-4
- make sure there's a newline at the end of yaboot.conf generated by 
  yabootconfig

* Wed Apr  9 2003 Jeremy Katz <katzj@redhat.com> 1.3.10-3
- try to read product name from /etc/redhat-release instead of hard coding
- add patch (from silo) to allow mounting dirty fs's instead of mounting 
  read-write

* Thu Apr  3 2003 Jeremy Katz <katzj@redhat.com> 1.3.10-2
- add patch from Peter Bergner <bergner@vnet.ibm.com> to add support for 
  ppc64 initrds (warning: breaks ppc32 initrds)

* Thu Mar 20 2003 Jeremy Katz <katzj@redhat.com> 1.3.10-1
- update to 1.3.10
- fix ofboot patch to use Red Hat Linux instead of Yellow Dog Linux
- include patch from Dan Burcaw for yabootconfig so that it can be used 
  from the installer

* Tue Jan 21 2003 Elliot Lee <sopwith@redhat.com> 1.3.8-1
- Update to new version

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 1.3.6-1b.2rh
- rebuild
- added ExclusiveArch

* Wed Mar 06 2002 Dan Burcaw <dburcaw@terrasoftsolutions.com>
- modify for YDL 2.2

* Fri Dec 07 2001 Dan Burcaw <dburcaw@terrasoftsolutions.com>
- update to 1.3.6

* Sat Oct 06 2001 Dan Burcaw <dburcaw@terrasoftsolutions.com>
- update to 1.3.4

* Sun Sep 30 2001 Dan Burcaw <dburcaw@terrasoftsolutions.com>
- updated to yaboot 1.3.3

* Tue Sep 25 2001 Dan Burcaw <dburcaw@terrasoftsolutions.com>
- add makefile patch

* Sun Sep 23 2001 Dan Burcaw <dburcaw@terrasoftsolutions.com>
- update to 1.3.1
- obsoletes ybin

* Thu Aug 08 2001 Dan Burcaw <dburcaw@terrasoftsolutions.com>
- updated to 1.2.3 per Ben H's urgent announcement
- removed obsoleted patches

* Tue Jan 16 2001 Hollis Blanchard <hollis@terrasoftsolutions.com>
- hacked out bug preventing manual boot from yaboot prompt (may break CHRP)
- removed ybin's man pages
- moved to /usr/lib/yaboot for ybin, FHS compliance
- changed permissions to 644 (can't run yaboot under Linux)

* Sat Nov 18 2000 Hollis Blanchard <hollis@terrasoftsolutions.com>
- updated to yaboot 0.9
- added man pages from ybin
- added sample yaboot.conf and bootscript (and README's)

* Sun Feb 27 2000 Dan Burcaw <dburcaw@terrasoftsolutions.com>
- modified for YDL

* Wed Jan 18 2000 Tom Rini <trini@kernel.crashing.org>
- created
